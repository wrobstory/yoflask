'use strict';

var mod = angular.module('yoflaskApp', ['ui.bootstrap']);

mod.controller('MainCtrl', ['$scope', '$http', function ($scope, $http) {

    $scope.dropdowns = {
        data: {
            isOpen: false
          },
        x: {
            isOpen: false
          },
        y: {
            isOpen: false
          }
        };
    $scope.dims = {
        x: null,
        y: null
      };
    $scope.dropdownNames = {
        'dataset': 'Dataset',
        'x': 'X-Dimension',
        'y': 'Y-Dimension'
      };
    $scope.chartTypes = ['Bar', 'Line', 'Scatter', 'Area'];
    $scope.dimensions = [];

    $scope.selectData = function(assetName){
        $http.post('/dimensions', {'name': assetName})
        .success(function(resp){
            $scope.dropdowns.data.isOpen = false;
            $scope.dropdownNames.dataset = assetName;
            $scope.dimensions = resp;
          });
      };

    $scope.selectDimension = function(axis, dim){
        $scope.dropdownNames[axis] = dim;
        $scope.dropdowns[axis].isOpen = false;
        $scope.dims[axis] = dim;
      };

  }]);
