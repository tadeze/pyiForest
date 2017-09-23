
from libcpp.vector cimport vector
from libcpp.map cimport map
from libcpp cimport bool
from libcpp.string cimport string

# c++ interface to cython
#import numpy as np
#import cPickle
#from collections import defaultdict

cdef extern from "../../cpp/FacadeForest.hpp":
  cdef cppclass FacadeForest:
        FacadeForest()
        void displayData()
        int trainForest(vector[vector[double]] &, int ,int,int,bool,bool,bool,double,int)
        void testForest(vector[vector[double]] &, bool)
        long factorial(int)
        vector[double]  getScore()
        vector[vector[double]] pathLength()
        vector[double] averageDepth()
        int getNTree()
        int getNSample()
        int getMaxDepth()
        bool isAdaptive()
        bool isRangeCheck()
        bool isRotate()
        int isValidModel()
        void save(string model_name)
        void load(string model_name)
        map[int,double] explanation(vector[double] &)

cdef extern from "../../cpp/Tree.hpp":
  cdef cppclass Tree:
        Tree()
        void iTree(vector[int] & ,vector[vector[double]],int,int,bool)
        double pathLength(vector[double] &)
        int maxTreeDepth()
        int getNodeSize()
        int getSplittingAtt()
        double getSplittingPoint()
        int getDepth()
        double getMinAttVal()
        double getMaxAttVal()
        map[int,double] explanation(vector[double] &)
        #Tree lChild()
        #Tree rChild()
        #void saveModel(string model_name)
        #void loadModel(string model_name,string forest_type)
cdef class IsolationForest:
    cdef FacadeForest *thisptr
    is_trained = False

    def __cinit__(self,traindf=None,ntree=100,nsample=512,maxheight=0,
                  rotate=False,adaptive=False,rangecheck=True,rho=0.01,stoplimit=5):
        """
        Create IsolationForest object. If parameters are given, the forest is trained as train_forest() method, otherwise empty
        object is created to be trained later.
        Args:
      _      traindf: Training dataset of ndarray(numpy matrix) format. Required field
            ntree: Number of trees used. Default 100
            nsample: Number of subsample size for training. Defualt 512
            maxheight: Maximum depth of the binary trees. Default 0 means grow tree until full isolation.
            rotate: Toggle for rotating forest or not. Default false.
            adaptive: Toggle for using adaptive method of growing trees. Default false.
            rangecheck: Toggle for rangecheck during scoring points. Default true.
            rho: Specify rho precision confidence interval for stopping criteria Value (0.01 to 0.08) works. Default value 0.01.Used only if adaptive is True.
            stoplimit:Number of common successive top K for adaptive process. Default 5.Used only if adaptiv is True
        >>ff = IsolationForest(traindf=train_data,ntree=100,nsample=100)

        Returns:

        """
        self.thisptr = new FacadeForest()
        if traindf is not None:
            self.train(traindf,ntree,nsample,maxheight,rotate,adaptive,rangecheck,rho,stoplimit)

    def __dealloc__(self):
        del self.thisptr


    def train(self,traindf,ntree=100,nsample=512,maxheight=0,rotate=False,
                     adaptive=False,rangecheck=True,rho=0.01,stoplimit=5):
        """
        Train Isolation Forest model.
        ff.train_forest(_traindf,_ntree=100,_nsample=512,_maxheight=0,_rotate=False,_adaptive=False,_rangecheck=True,_rho=0.01,_stoplimit=5):

        Args:
            traindf: Training dataset of ndarray(numpy matrix) format. Required field
            ntree: Number of trees used. Default 100
            nsample: Number of subsample size for training. Defualt 512
            maxheight: Maximum depth of the binary trees. Default 0 means grow tree until full isolation.
            rotate: Toggle for rotating forest or not. Default false.
            adaptive: Toggle for using adaptive method of growing trees. Default false.
            rangecheck: Toggle for rangecheck during scoring points. Default true.
            rho: Specify rho precision confidence interval for stopping criteria Value (0.01 to 0.08) works. Default value 0.01.Used only if adaptive is True.
            stoplimit:Number of common successive top K for adaptive process. Default 5.Used only if adaptiv is True

        Returns:

        """
        DataValidator.validate_dataset(traindf)
        if ntree<0:
            raise NameError("Number of trees cann't be less than 0")
        if ntree==0:
            print("You set 0 number of trees, then it is adaptive way of growing")
            adaptive=True
        if nsample >len(traindf):
            nsample=len(traindf)
            print("Number of samples cann't be greater than sample size,then data will be used")
        if maxheight<0:
            raise NameError("Max depth cann't be negative")
        if rho >1:
            raise NameError("rho value should be less than 1")
        is_trained = True

        return self.thisptr.trainForest(traindf,ntree,nsample,maxheight,rotate,adaptive,rangecheck,rho,stoplimit)

    def score(self,test_data,cmv=False):
        """
        Scored test data using trained anomaly detector.
        @param cmv : check missing value, default False
        Args:
            test_data: Testdata to score in ndarray format(numpy 2d-matrix), it should be the same dimension as training dataset.
        Returns: anomaly score value b/n 0 and 1.

        """
        #if not is_trained:
        #    raise NameError("Model not yet trained")
        #self.validate_model()

        if self.thisptr.isValidModel()==1:
            raise NameError("The iForest model is not yet trained.")
        DataValidator.validate_dataset(test_data)
        self.thisptr.testForest(test_data,cmv)
        return self.thisptr.getScore()

    def validate_model(self):
        if self.thisptr.isValidModel()==1:
            raise NameError("The iForest model is not yet trained.")
        if self.thisptr.isValidModel()==2:
            raise NameError("Test data not given")

    def anomaly_score(self):
        """

        Returns: Returns anomaly score from the trained model

        """
        self.validate_model() #check
        return self.thisptr.getScore()
    def path_length(self):
        """

        Returns: Returns path length of observations in all trees used.

        """
        self.validate_model(); #check
        return self.thisptr.pathLength()
    def average_depth(self):
        """

        Returns: Average depth(path length) across all trees of the forest.
        >> ff.average_depth() # returns average depth of all point passed in score method.
        """
        self.validate_model(); #check
        return self.thisptr.averageDepth()
    def save(self,model_name):
           """
           Save trained Isolation Forest model as binary or json.
           Args:
               model_name: model to save e.g. forest.bin or forest.json

           Returns:

           """
           return self.thisptr.save(model_name)

    def load(self,model_name,forest_type="iforest"):
       """
       Load trained iForest model from JSON file
       Args:
           model_name: path to the JSON model name
           forest_type: type of trained model. Default iforest

       Returns: Loads a trainded iForest model from saved file.

       """
       if DataValidator.validate_file_exists(model_name):
           return self.thisptr.load(model_name)

    def get_ntree(self):
       """

       Returns: number of trees used for building the forest

       """
       return self.thisptr.getNTree()
    def get_nsample(self):
       """

       Returns: sample size used for training

       """
       return self.thisptr.getNSample()
    def get_max_depth(self):
       """
       Returns: Maximum depth of the trees

       """
       return self.thisptr.getMaxDepth()

    def is_adaptive(self):
       """
       Return: True if the Forest is built with adaptive way
       """
       self.thisptr.isAdaptive()
    def is_range_check(self):
       """

       Returns: True if rangeCheck is set during scoring

       """
       return self.thisptr.isRangeCheck()
    def is_rotate(self):
       """

       Returns: True if rotation forest is used

       """
       return self.thisptr.isRotate()
    def is_valid_model(self):
       """

       Returns: True if the model is valid

       """
       return self.thisptr.isValidModel()
    def display_data(self):
        """

        Returns: displays the training data used.

        """
        return self.thisptr.displayData()
    def explanation(self,x):
        """
        Return: Explanations
        """
        return self.thisptr.explanation(x)

cdef class IsolationTree:
    cdef Tree *thisptr
    cdef train_points

    def __init__(self):
        self.thisptr =new Tree()
        self.train_points =[]
    def __dealloc__(self):
        del self.thisptr
    def iTree(self,train_index,train_data,height=0,maxheight=0,stopheight=False):
        """

        Returns: number of trees used for building the forest

        """
        return self.thisptr.iTree(train_index,train_data,height,maxheight,stopheight)

    def path_length(self,test_data):
        """
        Returns: Maximum depth of the trees

        """
        return self.thisptr.pathLength(test_data)
    def explanation(self,test_data):
        return self.thisptr.explanation(test_data)
    def max_depth(self):
        """
        Return: True if the Forest is built with adaptive way
        """
        return self.thisptr.maxTreeDepth()
    def get_nodesize(self):
        return self.thisptr.getNodeSize()
    def get_splittingAtt(self):
        return self.thisptr.getSplittingAtt()
    def get_splittingPoint(self):
        return self.thisptr.getSplittingPoint()
    def get_depth(self):
        return self.thisptr.getDepth()
    def get_minAttVal(self):
        return self.thisptr.getMinAttVal()
    def get_maxAttVal(self):
        return self.thisptr.getMaxAttVal()
