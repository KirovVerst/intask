(function () {
    'use strict';
    angular
        .module('application.users.services')
        .factory('Users', function ($http, $route, $resource) {
            return $resource('/api/users/:id', null, {
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

    angular
        .module('application.users.services')
        .factory('UsersInEvent', function ($http, $route, $resource) {
            return $resource('/api/events/:eventId/users/:userId', null, {
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
            })
        });

    angular
        .module('application.users.services')
        .factory('UsersInTask', function ($http, $route, $resource) {
            return $resource('/api/events/:eventId/tasks/:taskId/users/:userId', null, {
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
        })
})();