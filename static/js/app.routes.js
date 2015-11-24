/**
 * Created by Kirov on 19/11/15.
 */
(function () {
	'use strict';
	angular.module('application.routes')
		.config(function ($routeProvider) {
			$routeProvider.when('/', {
				templateUrl: '/static/templates/index.html'
			}).when('/login', {
				controller: 'AuthController',
				controllerAs: 'vm',
				templateUrl: '/static/templates/auth/login.html'
			}).when('/register', {
				controller: 'AuthController',
				controllerAs: 'vm',
				templateUrl: '/static/templates/auth/register.html'
			}).when('/events/new/', {
				controller: 'EventsController',
				controllerAs: 'vm',
				templateUrl: '/static/templates/events/new.html'
			}).when('/events/:eventId/', {
				controller: 'EventsController',
				controllerAs: 'vm',
				templateUrl: '/static/templates/events/event.html'
			}).when('/profile/', {
				templateUrl: '/static/templates/users/profile.html'
			}).otherwise({
				redirectTo: '/'
			});
		}).run(function ($rootScope, $location, Auth) {
		$rootScope.$on("$routeChangeStart", function (event, next, current) {
			if (Auth.getToken() == null) {
				if ((next.templateUrl === "/static/templates/register.html") ||
					(next.templateUrl === "/static/templates/login.html")) {
				} else {
					// no logged user, redirect to /login
					if (next.templateUrl === "/static/templates/login.html") {
					} else {
						$location.path("/login");
					}
				}
			} else {
				if ((next.templateUrl === "/static/templates/register.html") ||
					(next.templateUrl === "/static/templates/login.html")) {
					$location.path("/");
				}
			}
		})
	});
})();
