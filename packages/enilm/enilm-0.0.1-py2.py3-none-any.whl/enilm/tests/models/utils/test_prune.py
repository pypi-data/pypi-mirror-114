from unittest import TestCase

import tensorflow as tf
import numpy as np

import enilm as eml


class Conv1DPruneTest(TestCase):
    def create_model(self):
        # for input
        w = 12
        m = 2

        # for 1st conv1d
        p = 1
        c = 3
        k = 6

        # for 2nd conv1d
        p2 = 1
        c2 = 4
        k2 = 2

        inp = tf.keras.layers.Input(
            shape=(w, m),
            name='inp'
        )

        pad1 = tf.keras.layers.ZeroPadding1D(
            padding=p,
            name='pad1',
        )(inp)

        conv1 = tf.keras.layers.Conv1D(
            filters=c,
            kernel_size=k,
            name='conv1'
        )(pad1)

        pad2 = tf.keras.layers.ZeroPadding1D(
            padding=p2,
            name='pad2',
        )(conv1)

        conv2 = tf.keras.layers.Conv1D(
            filters=c2,
            kernel_size=k2,
            name='conv2'
        )(pad2)

        self.model = tf.keras.Model(
            inputs=inp,
            outputs=conv2
        )

    def setUp(self) -> None:
        self.create_model()

    def test_set_weights(self):
        filter_id = 1
        layer = self.model.get_layer('conv1')

        eml.models.utils.prune.set_weights(layer, filter_id, 0.001)
        w, b = layer.get_weights()

        self.assertTrue(np.all(w[:, :, filter_id] == 0.001))
        self.assertAlmostEqual(b[filter_id], 0.001)

    def test_to_prune(self):
        filter_id = 1
        layer = self.model.get_layer('conv1')

        eml.models.utils.prune.set_weights(layer, filter_id, 0)
        self.assertSetEqual(
            eml.models.utils.prune.to_prune(layer, 0.001),
            {filter_id}
        )

    def test_prune_conv(self):
        filter_id = 1
        layer = self.model.get_layer('conv1')
        threshold = 0.001

        eml.models.utils.prune.set_weights(layer, filter_id, 0)
        pruned_model = eml.models.utils.prune.prune(self.model, threshold)

        self.assertEqual(pruned_model.get_layer('conv1').filters, 2)

        # pruned model must have less parameters
        self.assertTrue(self.model.count_params() > pruned_model.count_params())

        # sanity check: both models produce same results
        batch_size = 1
        shape = list(self.model.input_shape)
        shape[0] = batch_size
        x = np.random.random(shape)

        # almost_equal (since threshold != exactly 0)
        y1 = self.model(x).numpy()
        y2 = pruned_model(x).numpy()

        # almost equal :) => models are almost the same
        self.assertTrue(np.max(np.abs(y1 - y2)) < 0.001)


class Conv2DPruneTest(TestCase):
    def create_model(self):
        # for input
        w = 12
        h = 6
        m = 2

        # for 1st conv2d
        p = (1, 1)
        c = 3
        k = (6, 4)

        # for 2nd conv2d
        p2 = (1, 1)
        c2 = 4
        k2 = (2, 2)

        # for 3rd conv2d
        p3 = (2, 1)
        c3 = 7
        k3 = (3, 1)

        inp = tf.keras.layers.Input(
            shape=(w, h, m),
            name='inp'
        )

        pad1 = tf.keras.layers.ZeroPadding2D(
            padding=p,
            name='pad1',
        )(inp)

        conv1 = tf.keras.layers.Conv2D(
            filters=c,
            kernel_size=k,
            name='conv1'
        )(pad1)

        pad2 = tf.keras.layers.ZeroPadding2D(
            padding=p2,
            name='pad2',
        )(conv1)

        conv2 = tf.keras.layers.Conv2D(
            filters=c2,
            kernel_size=k2,
            name='conv2'
        )(pad2)

        pad3 = tf.keras.layers.ZeroPadding2D(
            padding=p3,
            name='pad3',
        )(conv2)

        conv3 = tf.keras.layers.Conv2D(
            filters=c3,
            kernel_size=k3,
            name='conv3'
        )(pad3)

        self.model = tf.keras.Model(
            inputs=inp,
            outputs=conv3
        )

    def setUp(self) -> None:
        self.create_model()

        eml.models.utils.prune.set_weights(self.model.get_layer('conv2'), 1, 0)
        eml.models.utils.prune.set_weights(self.model.get_layer('conv2'), 3, 0)
        eml.models.utils.prune.set_weights(self.model.get_layer('conv3'), 1, 0)

    def test_to_prune(self):
        self.assertSetEqual(
            eml.models.utils.prune.to_prune(self.model.get_layer('conv1'), 0.001),
            set()
        )
        self.assertSetEqual(
            eml.models.utils.prune.to_prune(self.model.get_layer('conv2'), 0.001),
            {1, 3}
        )
        self.assertSetEqual(
            eml.models.utils.prune.to_prune(self.model.get_layer('conv3'), 0.001),
            {1}
        )

    def test_prune_conv(self):
        pruned_model = eml.models.utils.prune.prune(self.model, 0.001)

        # pruned model must have less parameters
        self.assertTrue(self.model.count_params() > pruned_model.count_params())

        # number of filters is reduced
        self.assertEqual(pruned_model.get_layer('conv2').filters, self.model.get_layer('conv2').filters - 2)
        self.assertEqual(pruned_model.get_layer('conv3').filters, self.model.get_layer('conv3').filters - 1)

        # sanity check: both models produce same results
        # note: since conv3 is pruned -> different output shape
        batch_size = 1
        shape = list(self.model.input_shape)
        shape[0] = batch_size
        x = np.random.random(shape)

        y1 = self.model(x).numpy()
        y2 = pruned_model(x).numpy()

        # in first model, since the weights of the second filter of conv3 is set to zero
        self.assertTrue(np.all(y1[:, :, :, 1] == 0))

        # remove it
        y1 = y1[:, :, :, [0, 2, 3, 4, 5, 6]]

        # almost equal :) => models are almost the same
        self.assertTrue(np.max(np.abs(y1 - y2)) < 0.001)


class DensePruneTest(TestCase):
    def create_model(self):
        # for input
        w = 12
        h = 6
        m = 2

        # for 1st conv2d
        p = (1, 1)
        c = 3
        k = (6, 4)

        # for 2nd conv2d
        p2 = (1, 1)
        c2 = 4
        k2 = (2, 2)

        # for 3rd conv2d
        p3 = (2, 1)
        c3 = 7
        k3 = (3, 1)

        inp = tf.keras.layers.Input(
            shape=(w, h, m),
            name='inp'
        )

        pad1 = tf.keras.layers.ZeroPadding2D(
            padding=p,
            name='pad1',
        )(inp)

        conv1 = tf.keras.layers.Conv2D(
            filters=c,
            kernel_size=k,
            name='conv1'
        )(pad1)

        pad2 = tf.keras.layers.ZeroPadding2D(
            padding=p2,
            name='pad2',
        )(conv1)

        conv2 = tf.keras.layers.Conv2D(
            filters=c2,
            kernel_size=k2,
            name='conv2'
        )(pad2)

        pad3 = tf.keras.layers.ZeroPadding2D(
            padding=p3,
            name='pad3',
        )(conv2)

        conv3 = tf.keras.layers.Conv2D(
            filters=c3,
            kernel_size=k3,
            name='conv3'
        )(pad3)

        flat = tf.keras.layers.Flatten(
            name='flat'
        )(conv3)

        dense1 = tf.keras.layers.Dense(
            units=16,
            name='dense1',
        )(flat)

        dense2 = tf.keras.layers.Dense(
            units=1,
            name='dense2',
        )(dense1)

        self.model = tf.keras.Model(
            inputs=inp,
            outputs=dense2,
        )

    def setUp(self) -> None:
        self.create_model()

        eml.models.utils.prune.set_weights(self.model.get_layer('dense1'), 13, 0)
        eml.models.utils.prune.set_weights(self.model.get_layer('dense1'), 2, 0)

    def test_get_prune(self):
        self.assertSetEqual(
            eml.models.utils.prune.to_prune(self.model.get_layer('dense1'), 0.001),
            {13, 2}
        )

    def test_prune_dense(self):
        pruned_model = eml.models.utils.prune.prune(self.model, 0.001)

        # pruned model must have less parameters
        self.assertTrue(self.model.count_params() > pruned_model.count_params())

        # number of filters is reduced
        self.assertEqual(
            pruned_model.get_layer('dense1').units,
            self.model.get_layer('dense1').units - 2
        )

        # sanity check: both models produce same results
        # note: since conv3 is pruned -> different output shape
        batch_size = 1
        shape = list(self.model.input_shape)
        shape[0] = batch_size
        x = np.random.random(shape)

        y1 = self.model(x).numpy()
        y2 = pruned_model(x).numpy()

        # almost equal :) => models are almost the same
        self.assertTrue(np.max(np.abs(y1 - y2)) < 0.001)


class ConvDensePruneTest(TestCase):
    def create_model(self):
        # for input
        w = 12
        h = 6
        m = 2

        # for 1st conv2d
        p = (1, 1)
        c = 3
        k = (6, 4)

        # for 2nd conv2d
        p2 = (1, 1)
        c2 = 4
        k2 = (2, 2)

        # for 3rd conv2d
        p3 = (2, 1)
        c3 = 7
        k3 = (3, 1)

        inp = tf.keras.layers.Input(
            shape=(w, h, m),
            name='inp'
        )

        pad1 = tf.keras.layers.ZeroPadding2D(
            padding=p,
            name='pad1',
        )(inp)

        conv1 = tf.keras.layers.Conv2D(
            filters=c,
            kernel_size=k,
            name='conv1'
        )(pad1)

        pad2 = tf.keras.layers.ZeroPadding2D(
            padding=p2,
            name='pad2',
        )(conv1)

        conv2 = tf.keras.layers.Conv2D(
            filters=c2,
            kernel_size=k2,
            name='conv2'
        )(pad2)

        pad3 = tf.keras.layers.ZeroPadding2D(
            padding=p3,
            name='pad3',
        )(conv2)

        conv3 = tf.keras.layers.Conv2D(
            filters=c3,
            kernel_size=k3,
            name='conv3'
        )(pad3)

        flat = tf.keras.layers.Flatten(
            name='flat'
        )(conv3)

        dense1 = tf.keras.layers.Dense(
            units=16,
            name='dense1',
        )(flat)

        dense2 = tf.keras.layers.Dense(
            units=1,
            name='dense2',
        )(dense1)

        self.model = tf.keras.Model(
            inputs=inp,
            outputs=dense2,
        )

    def setUp(self) -> None:
        self.create_model()

        eml.models.utils.prune.set_weights(self.model.get_layer('conv2'), 1, 0)
        eml.models.utils.prune.set_weights(self.model.get_layer('conv2'), 3, 0)
        eml.models.utils.prune.set_weights(self.model.get_layer('conv3'), 1, 0)

        eml.models.utils.prune.set_weights(self.model.get_layer('dense1'), 2, 0)
        eml.models.utils.prune.set_weights(self.model.get_layer('dense1'), 13, 0)

    def test_prune(self):
        pruned_model = eml.models.utils.prune.prune(self.model, 0.001)

        # pruned model must have less parameters
        self.assertTrue(self.model.count_params() > pruned_model.count_params())

        # sanity check: both models produce same results
        # note: since conv3 is pruned -> different output shape
        batch_size = 1
        shape = list(self.model.input_shape)
        shape[0] = batch_size
        x = np.random.random(shape)

        y1 = self.model(x).numpy()
        y2 = pruned_model(x).numpy()

        # almost equal :) => models are almost the same
        self.assertTrue(np.max(np.abs(y1 - y2)) < 0.001)
