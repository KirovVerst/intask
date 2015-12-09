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
                controllerAs: 'vm'
            }).when('/login', {
                controller: 'AuthController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/auth/login.html'
            }).when('/register', {
                controller: 'AuthController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/auth/register.html'
            }).when('/events/:eventId/', {
                controller: 'CurrentEventController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/events/event.html'
            }).when('/profile/', {
                controller: 'UsersController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/users/profile.html'
            }).when('/events/:eventId/tasks/new/', {
                controller: 'TasksController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/tasks/new.html'
            }).otherwise({
                redirectTo: '/'
            });
        }).run(function ($rootScope, $location, Auth) {
        $rootScope.$on("$routeChangeStart", function (event, next, current) {
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
        })
    });
})();
