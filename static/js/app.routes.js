/**
 * Created by Kirov on 19/11/15.
 */
(function () {
    'use strict';
    angular.module('application.routes')
        .config(function ($routeProvider) {
            $routeProvider.when('/', {
                templateUrl: '/static/templates/index.html',
                controller: 'EventsController',
                controllerAs: 'vm',
                reloadOnSearch: false
            }).when('/login', {
                controller: 'AuthController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/auth/login.html'
            }).when('/register', {
                controller: 'AuthController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/auth/register.html',
                reloadOnSearch: false
            }).when('/profile/', {
                controller: 'UsersController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/users/profile.html'
            }).otherwise({
                redirectTo: '/'
            });
        }).run(function ($rootScope, $location, Auth, $route) {
        $rootScope.$on("$routeChangeStart", function (event, next, current) {
            var original = $location.path;
            $location.path = function (path, reload) {
                if (reload === false) {
                    var lastRoute = $route.current;
                    var un = $rootScope.$on('$locationChangeSuccess', function (event) {
                        $route.current = lastRoute;
                        un();
                    });
                }
                return original.apply($location, [path]);
            };
            if (Auth.getToken() == null) {
                if ((next.templateUrl === "/static/templates/auth/register.html") ||
                    (next.templateUrl === "/static/templates/auth/login.html")) {
                } else {
                    // no logged user, redirect to /login
                    if (next.templateUrl === "/static/templates/auth/login.html") {
                    } else {
                        $location.path("/login");
                    }
                }
            } else {
                if ((next.templateUrl === "/static/templates/auth/register.html") ||
                    (next.templateUrl === "/static/templates/auth/login.html")) {
                    $location.path("/");
                }
            }
        });
    });
})();
