/**
 * Created by Kirov on 19/11/15.
 */
(function () {
    'use strict';

    angular.module('application.auth.services').
    service('Auth', function ($http, $location, $q, $window) {
        var Auth = {
            getToken: function () {
                return $window.localStorage.getItem('token');
            },

            setToken: function (token) {
                $window.localStorage.setItem('token', token);
            },

            setEmail: function (email) {
                $window.localStorage.setItem('email', email);
            },

            setUserId: function (id) {
                $window.localStorage.setItem('id', id);
            },

            getUserId: function () {
                return $window.localStorage.getItem('id');
            },

            deleteUserId: function () {
                $window.localStorage.removeItem('id');
            },


            getEmail: function () {
                return $window.localStorage.getItem('email');
            },
            deleteToken: function () {
                $window.localStorage.removeItem('token');
            },
            deleteEmail: function () {
                $window.localStorage.removeItem('email');
            },
            login: function (email, password) {
                var deferred = $q.defer();

                $http.post('/api/auth/login/', {
                    email: email, password: password
                }).success(function (response, status, headers, config) {
                    if (response.token) {
                        Auth.setToken(response.token);
                        Auth.setEmail(response.email);
                        Auth.setUserId(response.id);
                    }
                    $window.location = '/';
                    deferred.resolve(response, status, headers, config);
                }).error(function (response, status, headers, config) {
                    deferred.reject(response, status, headers, config);
                });

                return deferred.promise;
            },
            logout: function () {
                Auth.deleteToken();
                Auth.deleteEmail();
                Auth.deleteUserId();
                $window.location = '/';
            },
            register: function (email, password, first_name, last_name) {
                var deferred = $q.defer();

                $http.post('/api/users/', {
                    password: password, email: email,
                    first_name: first_name, last_name: last_name
                }).success(function (response, status, headers, config) {
                    if (response.token) {
                        Auth.setToken(response.token);
                        Auth.setEmail(response.email);
                        Auth.setUserId(response.id);
                        $window.location = '/';
                    }

                    deferred.resolve(response, status, headers, config);
                }).error(function (response, status, headers, config) {
                    deferred.reject(response, status, headers, config);
                });

                return deferred.promise;
            }
        };

        return Auth;
    });
})();
