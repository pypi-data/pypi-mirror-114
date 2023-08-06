from unittest import TestCase

import enilm


class TestConfig(TestCase):
    def setUp(self) -> None:
        tz = enilm.nilmdt.get_tzinfo_from_ds(enilm.etypes.Datasets.UKDALE)
        self.config = enilm.config.ExpConfig(
            exp_n=41,
            appliances=['fridge', 'microwave'],
            win_size=599,
            sample_period=60,
            repeats=4,
            epochs=80,
            batch_size=512,
            shuffle=False,
            validation_split=0.2,
            model_id='s2p_seq_mtl4',
            train=[
                enilm.config.DataSel(
                    houses=[1, 2],
                    dataset=enilm.etypes.Datasets.UKDALE,
                    sections={
                        1: [enilm.nilmdt.get_month_timeframe(2011, 12, tz),
                            enilm.nilmdt.get_month_timeframe(2012, 3, tz)],
                        2: [enilm.nilmdt.get_month_timeframe(2012, 3, tz)],
                    }
                )
            ],
            test=[
                enilm.config.DataSel(
                    houses=[4],
                    dataset=enilm.etypes.Datasets.UKDALE,
                ),
            ],
        )

    def test_asdict(self):
        config_dict = self.config.asdict()
        self.assertEqual(config_dict['train'][0]['dataset'], 'UKDALE')
        self.assertEqual(config_dict['test'][0]['dataset'], 'UKDALE')
        self.assertListEqual(config_dict['train'][0]['houses'], [1, 2])
        self.assertListEqual(config_dict['test'][0]['houses'], [5])
        self.assertIsNone(config_dict['test'][0]['sections'])

    def test_to_json(self):
        config_json = self.config.to_json()
        config_from_json = enilm.config.ExpConfig.from_json(config_json)
        self.assertTrue(self.config == config_from_json)
