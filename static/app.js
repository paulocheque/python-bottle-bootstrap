(function () {
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

    .config(['$sceDelegateProvider', function ($sceDelegateProvider) {
        $sceDelegateProvider.resourceUrlWhitelist(['self', new RegExp('^(http[s]?):\/\/.+$')]);
    }])

    .controller('ProjectCtrl', function($scope, $http, $window) {
        $scope.lastDay = null;
        $scope.currentDay = null;
        $scope.nextDay = null;
        $scope.lastUpdate = null;
        $scope.nextUpdate = null;

        $scope.links = []
        $scope.messages = []

        $scope.getLinks = function(date) {
            var day = date.getDate();
            var month = date.getMonth()+1; //January is 0!
            var year = date.getFullYear();
            $http.get("/api/v1/links/" + year + "/" + month + "/" + day).success(function (data) {
                // console.log(data)
                $scope.links = JSON.parse(data['links'])
                $scope.currentDay = new Date(data['currentDay'])
                $scope.lastDay = new Date(data['lastDay'])
                $scope.nextDay = new Date(data['nextDay'])
                $scope.lastUpdate = new Date(data['lastUpdate'])
                $scope.nextUpdate = new Date(data['nextUpdate'])
            });
        }

        var today = new Date()
        $scope.getLinks(today)

        // Keyboard shortcuts

        document.onkeydown = function(evt) {
            evt = evt || window.event;
            switch (evt.keyCode) {
                case 37:
                    leftArrowPressed();
                    break;
                case 39:
                    rightArrowPressed();
                    break;
            }
        };

        function leftArrowPressed() {
            console.log('left')
        }

        function rightArrowPressed() {
            console.log('right')
        }
    })

    .controller('TagsCtrl', function($scope, $http, $window) {
        $scope.tags = []
        $scope.languages = []

        $http.get("/api/v1/tags").success(function (data) {
            // console.log(data)
            $scope.languages = data['languages']
            $scope.tags = JSON.parse(data['tags'])
        });

    })
})();
