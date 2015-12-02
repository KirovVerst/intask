(function () {
	'use strict';
	angular
		.module('application.tasks.services', ['ngResource'])
		.factory('Tasks', function ($http, $route, $resource) {
			return $resource('/api/events/:eventId/tasks/:taskId/' + '/');
		});
})();