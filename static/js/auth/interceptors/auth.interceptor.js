/**
 * Created by Kirov on 19/11/15.
 */
(function () {
	'use strict';

	angular.module('application.auth.interceptors')
		.service('AuthInterceptor', function ($injector, $location) {
			return {
				request: function (config) {
					var Auth = $injector.get('Auth');
					var token = Auth.getToken();

					if (token) {
						config.headers['Authorization'] = 'Token ' + token;
					}
					return config;
				},
				responseError: function (response) {
					if (response.status === 403) {
						$location.path('/login');
					}
					return response;
				}
			};
		});
})();
