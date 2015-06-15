(function () {
    'use strict';

    angular.module('project', ['ui', 'ngRoute'])

    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    })

    .config(function($routeProvider) {
        var date = new Date()
        var day = date.getDate()
        var month = date.getMonth() + 1 //January is 0!
        var year = date.getFullYear()
        var today = year + "/" + month + "/" + day + "/"

        $routeProvider
        .when('/', {
            redirectTo: today
        })
        .when('/:year/:month/:day/', {
            templateUrl: '/static/pages/links.html',
            controller: 'LinksOfTheDayCtrl'
        })
        .when('/tags/', {
            templateUrl: '/static/pages/tags.html',
            controller: 'TagsCtrl'
        })
        .when('/tags/:tag_name/', {
            templateUrl: '/static/pages/links_of_the_tag.html',
            controller: 'LinksOfTheTagCtrl'
        })
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

    .controller('ProjectCtrl', function($scope, $http) {
    })

    .controller('LinksOfTheDayCtrl', function($scope, $http, $routeParams) {
        $scope.currentDay = moment($routeParams.year + "-" + $routeParams.month + "-" + $routeParams.day)._d
        $scope.lastDay = moment($scope.currentDay).add(-1, 'days')._d
        $scope.nextDay = moment($scope.currentDay).add(+1, 'days')._d
        $scope.lastUpdate = null;
        $scope.nextUpdate = null;

        $scope.links = []
        $scope.messages = []

        $scope.getLinks = function(date) {
            $scope.currentDay = moment(date)._d
            $scope.lastDay = moment($scope.currentDay).add(-1, 'days')._d
            $scope.nextDay = moment($scope.currentDay).add(+1, 'days')._d

            var day = date.getDate()
            var month = date.getMonth() + 1 //January is 0!
            var year = date.getFullYear()
            date = year + "/" + month + "/" + day
            $http.get("/api/v1/links/day/" + date).success(function (data) {
                // console.log(data)
                $scope.links = JSON.parse(data['links'])
                $scope.lastUpdate = new Date(data['lastUpdate'])
                $scope.nextUpdate = new Date(data['nextUpdate'])
            });
        }

        $scope.getLinks($scope.currentDay)
        $('[data-toggle="tooltip"]').tooltip()

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

    .controller('TagsCtrl', function($scope, $http) {
        $scope.tags = []
        $scope.languages = []

        $http.get("/api/v1/tags").success(function (data) {
            // console.log(data)
            $scope.languages = data['languages']
            $scope.tags = JSON.parse(data['tags'])
        });
    })

    .controller('LinksOfTheTagCtrl', function($scope, $http, $routeParams) {
        $scope.links = []

        $http.get("/api/v1/links/tag/" + $routeParams.tag_name).success(function (data) {
            console.log(data)
            $scope.links = data
        });
    })




})();
