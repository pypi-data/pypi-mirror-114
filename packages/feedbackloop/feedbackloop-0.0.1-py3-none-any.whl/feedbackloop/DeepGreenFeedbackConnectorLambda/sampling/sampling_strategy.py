# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import logging
import heapq
import math
import random
from abc import ABCMeta, abstractmethod
from numbers import Number

FLOAT_COMPARISON_TOLERANCE = 1e-08

STRATEGY_RANDOM_SAMPLING = "RANDOM_SAMPLING"
STRATEGY_LEAST_CONFIDENCE = "LEAST_CONFIDENCE"
STRATEGY_MARGIN = "MARGIN"
STRATEGY_ENTROPY = "ENTROPY"
SAMPLING_STRATEGIES = {
    STRATEGY_RANDOM_SAMPLING, 
    STRATEGY_LEAST_CONFIDENCE, 
    STRATEGY_MARGIN,
    STRATEGY_ENTROPY
}

class GreengrassInvalidSamplingStrategyException(Exception):
    '''
        Raised when there is an attempt to create and invalid
        sampling strategy instance.
    '''
    pass

class SamplingStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def should_use_sample(self, model_prediction):
        pass

class SamplingPercentage(object):
    def __init__(self, value):
        # Check existence using number because threshold can be 0 which
        # evaluates to False
        if not isinstance(value, Number):
            raise GreengrassInvalidSamplingStrategyException(
                "Failed to read percentage value. Requires value to be configured and to be a number."
            )

        if not 0.0 <= value <= 1.0:
            raise GreengrassInvalidSamplingStrategyException(
                "Invalid percentage value: {}. Value must be 0.0 <= percentage <= 1.0".format(str(value))
            )

        self._value = value

    @property
    def value(self):
        return self._value

class RandomSamplingStrategy(SamplingStrategy):
    '''
        SamplingStrategy that randomly selects samples
        to be labeled based on rate. Note: This
        strategy disregards any model prediction that is
        supplied.
    '''
    
    def __init__(self, rate, seed=None):
        try:
            rate_percentage = SamplingPercentage(rate)
        except Exception as e:
            logging.warn("Failed to create RandomSamplingStrategy because of invalid rate. Failed with exception type: {}, error: {}".format(type(e).__name__, e))
            raise e

        self._rate = rate_percentage.value

        # Used for testing
        if seed:
            random.seed(seed)

    def should_use_sample(self, model_prediction):
        '''
            Returns whether a sample should be used based on 
            rate alone. The model_prediction parameter is 
            disregarded.
        '''
        random_value = random.random()
        should_use_sample = random_value < self._rate
        logging.info("RandomSamplingStrategy returning {} for should use sample. Should use sample if random generated value ({}) is less than sampling rate ({}).".format(
            str(should_use_sample), str(random_value), str(self._rate)
        ))
        return should_use_sample

class LeastConfidenceSamplingStrategy(SamplingStrategy):
    '''
        SamplingStrategy that selects samples whose max
        confidence falls below some threshold.

        Ex. For model prediction: [.2, .2, .4, .2] and
            threshold: .6

        Max confidence = .4

        Use sample if max confidence (.4) <= threshold (.6)

    '''
    def __init__(self, threshold):
        try:
            threshold_percentage = SamplingPercentage(threshold)
        except Exception as e:
            logging.warn("Failed to create LeastConfidenceSamplingStrategy because of invalid threshold. Failed with exception type: {}, error: {}".format(type(e).__name__, e))
            raise e            

        self._threshold = threshold_percentage.value

    def should_use_sample(self, model_prediction):
        '''
            Returns whether a sample should be used based on 
            threshold and the model_prediction's highest 
            confidence probability.
        '''
        max_confidence = max(model_prediction)
        should_use_sample = max_confidence < self._threshold
        logging.info("LeastConfidenceSamplingStrategy returning {} for should use sample. Should use sample if the highest prediction confidence probability ({}) is less than threshold ({}).".format(
            str(should_use_sample), str(max_confidence), str(self._threshold)
        ))
        return should_use_sample

class MarginSamplingStrategy(SamplingStrategy):
    '''
        SamplingStrategy that selects samples whose top two
        confidence probabiltities fall within a some threshold.

        Ex. For model prediction: [.3, .35, .34, .01] and
            threshold: .02:

        Top two confidence probabilities = [.35, .34]
        Margin = .01 = .35 - .34

        Use sample if margin (.01) <= threshold (.02)
    '''
    def __init__(self, threshold):
        try:
            threshold_percentage = SamplingPercentage(threshold)
        except Exception as e:
            logging.warn("Failed to create MarginSamplingStrategy because of invalid threshold. Failed with exception type: {}, error: {}".format(type(e).__name__, e))
            raise e

        self._threshold = threshold_percentage.value

    def should_use_sample(self, model_prediction):
        '''
           Returns whether a sample should be used based on 
           threshold and the model prediction's top two 
           highest confidence probabilities.
        '''
        top_two_highest_confidence = heapq.nlargest(2, model_prediction)
        highest_confidence = top_two_highest_confidence[0]
        second_highest_confidence = top_two_highest_confidence[1]
        margin = abs(highest_confidence - second_highest_confidence)
        # Using less than (as opposed to <=) because we are comparing
        # floats.
        should_use_sample = margin < self._threshold
        logging.info("MarginSamplingStrategy returning {} for should use sample. Should use sample if the prediction's top two highest confidence probabilities ({}, {}) have a margin ({}) within threshold ({}).".format(
            str(should_use_sample), str(highest_confidence), str(second_highest_confidence), str(margin), str(self._threshold)
        ))
        return should_use_sample

class EntropySamplingStrategy(SamplingStrategy):
    '''
        SamplingStrategy that selects samples whose entropy
        is above some threshold.

        Ex. For model prediction: [.5, .25, .25] and
            threshold: 0.75:

        Entropy for prediction = 1.03972

        Use sample if entropy (1.03972) > threshold (0.75)
    '''
    def __init__(self, threshold):
        if not threshold:
            raise GreengrassInvalidSamplingStrategyException("Failed to create EntropySamplingStrategy. Sampling strategy threshold must be defined.")
        
        if not isinstance(threshold, Number):
            raise GreengrassInvalidSamplingStrategyException("Failed to create EntropySamplingStrategy. Sampling strategy threshold must be a number.")

        self._threshold = threshold
    
    @staticmethod
    def _calculate_entropy(model_prediction):
        def _single_class_entropy(class_probability):
            if class_probability > 0:
                return class_probability * math.log(class_probability)
            elif class_probability == 0:
                return 0
            else:
                # Scipy returns -inf when negative probabilies are supplied. We 
                # throw here to let customers know that entropy can't be calculated.
                raise ValueError("Could not calculate entropy. Found negative class probability: {}".format(class_probability))

        # Normalize array to 1.0 first - this is how scipy does 
        # this too. See:
        # https://github.com/scipy/scipy/blob/v1.2.1/scipy/stats/_distn_infrastructure.py#L2515-L2556
        model_prediction_probability_sum = sum(model_prediction)
        if abs(1.0 - model_prediction_probability_sum) < FLOAT_COMPARISON_TOLERANCE:
            normalized = model_prediction
        elif model_prediction_probability_sum == 0.0:
            raise ValueError("Could not calculate entropy. Sum of model predictions must not be zero.")
        else:
            normalized = [probability_of_class / sum(model_prediction) for probability_of_class in model_prediction]

        entropy = -sum(_single_class_entropy(class_probability) for class_probability in normalized)
        return entropy

    def should_use_sample(self, model_prediction):
        '''
            Returns whether a sample should be used based on
            threshold and the model prediction's normalized
            entropy. Returns true if the calculated entropy is
            greater than the threshold.
        '''
        entropy = EntropySamplingStrategy._calculate_entropy(model_prediction)
        should_use_sample = entropy > self._threshold
        logging.info("EntropySamplingStrategy returning {} for should use sample. Should use sample if entropy ({}) is greater than threshold ({}).".format(
            str(should_use_sample), str(entropy), str(self._threshold)
        ))
        return should_use_sample

class SamplingStrategyFactory(object):
    '''
        Responsible for creating instances of SamplingStrategy.
    '''
    @staticmethod
    def create_instance(strategy_name, rate=None, threshold=None):
        '''
            Creates an instance of a sampling strategy that 
            implements SamplingStrategy. Throws when strategy 
            name is not one defined in SAMPLING_STRATEGIES.
        '''
        if strategy_name == STRATEGY_RANDOM_SAMPLING:
            return RandomSamplingStrategy(rate)
        elif strategy_name == STRATEGY_LEAST_CONFIDENCE:
            return LeastConfidenceSamplingStrategy(threshold)
        elif strategy_name == STRATEGY_MARGIN:
            return MarginSamplingStrategy(threshold)
        elif strategy_name == STRATEGY_ENTROPY:
            return EntropySamplingStrategy(threshold)
        else:
            raise GreengrassInvalidSamplingStrategyException("Failed to create SamplingStrategy instance. Found invalid sampling strategy: {}. Sampling strategy must be one of: {}".format(
                str(strategy_name), str(SAMPLING_STRATEGIES)
            ))

        