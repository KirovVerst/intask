/**
 * Created by Kirov on 19/11/15.
 */
(function () {
    'use strict';

    angular.module('application.auth.controllers')
        .controller('AuthController', function (Auth, $location) {
            var vm = this;

            vm.isLoggedIn = !!Auth.getToken();

            vm.init = function () {
                vm.params = $location.search();
                vm.email = vm.params.email;
            };

            vm.login = function () {
                Auth.login(vm.email, vm.password);
            };

            vm.register = function () {
                Auth.register(vm.email, vm.password, vm.first_name, vm.last_name);
            };

            vm.logout = function () {
                Auth.logout();
            };

            vm.email = Auth.getEmail();


        })
})();
