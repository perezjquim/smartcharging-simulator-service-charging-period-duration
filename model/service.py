from nameko.events import EventDispatcher
from nameko.rpc import rpc

from model.exceptions import NotFound

import json

import tensorflow as tf

class ModelService:

    CHARGING_PERIOD_DURATION_AVG = 142.889
    CHARGING_PERIOD_DURATION_STDDEV = 44.898

    name = 'model_charging_period_duration'

    event_dispatcher = EventDispatcher()

    @rpc
    def get_charging_period_duration(self):
        charging_period_duration = self.generate_charging_period_duration()
        response = json.dumps({'charging_period_duration': charging_period_duration})
        return response

    def generate_charging_period_duration(self):
        shape = [1,1]
        min_charging_period_duration = self.CHARGING_PERIOD_DURATION_AVG - self.CHARGING_PERIOD_DURATION_STDDEV
        max_charging_period_duration = self.CHARGING_PERIOD_DURATION_AVG + self.CHARGING_PERIOD_DURATION_STDDEV

        tf_random = tf.random.uniform(
                shape=shape,
                minval=min_charging_period_duration,
                maxval=max_charging_period_duration,
                dtype=tf.dtypes.float32,
                seed=None,
                name=None
        )
        tf_var = tf.Variable( tf_random )

        tf_init = tf.initialize_all_variables()
        tf_session = tf.Session()
        tf_session.run(tf_init)

        tf_return = tf_session.run(tf_var)
        charging_period_duration = float( tf_return[ 0 ][ 0 ] )

        return charging_period_duration
