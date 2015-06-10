'use strict';

angular.module('project', ['ui'])

.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})

.config(['$compileProvider', function ($compileProvider) {
    $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|local|data):/);
}])

.run(function($http) {
  $http.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
})

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
}])

.controller('ProjectCtrl', function($scope, $http, $window) {
    $scope.data = []

    $http.get("/api/v1/endpoint?format=json").success(function (data) {
        // console.log(data)
        $scope.data = data
        // data.forEach(function(d) {
        //     $scope.data.push(d)
        // })
    });

    $scope.func = function() {
    }

})
