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
    var today = new Date();
    var day = today.getDate();
    var month = today.getMonth()+1; //January is 0!
    var year = today.getFullYear();

    $scope.date = year + "/" + month + "/" + day;
    $scope.nextUpdate = "06:00"
    $scope.links = []
    $scope.messages = []

    $http.get("/api/v1/links/" + year + "/" + month + "/" + day).success(function (data) {
        console.log(data)
        $scope.links = data
        // data.forEach(function(d) {
        //     $scope.data.push(d)
        // })
    });

    $scope.getViews = function(views) {
        return views + Math.floor((Math.random() * 5000) + 1000);
    }

})
