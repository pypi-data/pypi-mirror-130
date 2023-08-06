from outer.Object import File, Dir, Object
from outer.BluePrint import BluePrint


class BluePrintSample(BluePrint):
    def __init__(self, key='1'):
        super().__init__(key=key)

        self.ROOT = self.sub_dir('{}_UNet')
        # define file or dir
        self.LOG_MAIN = self.ROOT.sub_file('run.log')
        self.LOG_TENSORBOARD = self.ROOT.sub_dir('event')
        self.FILE_CHECKPOINT = self.ROOT.sub_file('model_{}.pkl')

        self.TRAIN_DIR = self.ROOT.sub_file('train')
        self.TRAIN_IMG_OUTPUT = self.TRAIN_DIR.sub_dir('image')
        self.TRAIN_LABEL_OUTPUT = self.TRAIN_DIR.sub_dir('label')
        self.TRAIN_GT_OUTPUT = self.TRAIN_DIR.sub_dir('gt')

        # recall father init
        self.init()