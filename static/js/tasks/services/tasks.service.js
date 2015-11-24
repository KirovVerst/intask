(function () {
	'use strict';
	angular
		.module('application.tasks.services', ['ngResource'])
		.factory('Tasks', function ($http, $route, $resource) {
			return $resource();
		});
})();