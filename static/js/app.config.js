/**
 * Created by Kirov on 19/11/15.
 */
(function () {
	'use strict';
	angular.module('application.config')
		.config(function ($httpProvider, $locationProvider) {
			$locationProvider.html5Mode(true).hashPrefix('!');
			$httpProvider.interceptors.push('AuthInterceptor');
		});
})();
