(function () {
	'use strict';
	angular
		.module('application.events.services', ['ngResource'])
		.factory('Events', function ($http, $route, $resource) {
            return $resource('/api/events/:id', null, {
                'update': {
                    method: 'PATCH',
                    interceptor: {
                        response: function (response) {
                            var result = response.resource;
                            result.$status = response.status;
                            return result;
                        }
                    }
                }
            }, {
                stripTrailingSlashes: false
            });
        });
})();