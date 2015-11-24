(function () {
	'use strict';
	angular
		.module('application.users.services', ['ngResource'])
		.factory('Users', function ($http, $route, $resource) {
			return $resource();
		});
})();