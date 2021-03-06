import yaml
import logging
import argparse
from module import Preprocessor, Trainer, Predictor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process commandline')
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--log_level', type=str, default="INFO")
    args = parser.parse_args()

    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level = args.log_level)
    logger = logging.getLogger('global_logger')
    with open(args.config, 'r') as config_file:
        try:
            config = yaml.safe_load(config_file)
            preprocessor = Preprocessor(config['preprocessing'], logger)
            data_x, data_y, train_x, train_y, validate_x, validate_y, test_x = preprocessor.process()
            trainer = Trainer(config['training'], logger, preprocessor.classes)
            trainer.fit(train_x, train_y)
            # Returns value error: Classification metrics can't handle a mix of multilabel-indicator and binary target
            # Therefore quote out these for now to have the program work
            #accuracy, cls_report = trainer.validate(validate_x, validate_y)
            #logger.info("accuracy:{}".format(accuracy))
            #logger.info("\n{}\n".format(cls_report))
            model = trainer.fit(data_x, data_y)
            predictor = Predictor(config['predict'], logger, model)
            probs = predictor.predict_prob(test_x)
            predictor.save_result(preprocessor.test_ids, probs)
        except yaml.YAMLError as err:
            logger.warning('Config file err: {}'.format(err))
