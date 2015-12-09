(function () {
    'use strict';
    angular
        .module('application.subtasks.services', ['ngResource'])
        .factory('Subtasks', function ($http, $route, $resource) {
            return $resource('/api/events/:eventId/tasks/:taskId/subtasks/:subtaskId/', null, {
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