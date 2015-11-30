(function () {
	'use strict';
	angular
		.module('application.users.services')
		.factory('Users', function ($http, $route, $resource) {
			return $resource('/api/users/:id', null,{
				'update': { method:'PATCH' }
			});
		});
})();