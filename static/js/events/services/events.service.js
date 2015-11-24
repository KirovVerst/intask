(function () {
	'use strict';
	angular
		.module('application.events.services', ['ngResource'])
		.factory('Events', function ($http, $route, $resource) {
			return $resource('/api/events/:id')
		});
})();