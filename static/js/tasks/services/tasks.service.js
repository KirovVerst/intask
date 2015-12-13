(function () {
    'use strict';
    angular
        .module('application.tasks.services', ['ngResource'])
        .factory('Tasks', function ($http, $route, $resource) {
            return $resource('/api/events/:eventId/tasks/:taskId', null, {
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