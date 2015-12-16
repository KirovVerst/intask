(function () {
    'use strict';

    angular
        .module('application.users.controllers')
        .controller('UsersController', function (Users, $http, $route , $scope, Auth, $window, $routeParams, $location) {

            var vm = this;
            vm.isLoggedIn = !!Auth.getToken();

            vm.profile = Users.get({id: Auth.getUserId()});

            vm.updateProfile = function () {
                vm.isSent = true;
                Users.update({id: vm.profile.id}, {
                    first_name: vm.profile.first_name,
                    last_name: vm.profile.last_name
                }).$promise.then(function (response) {
                    if (response.$status == 200) {
                        vm.errors = null;
                        vm.message = "Профиль обновлен";
                        vm.class = "alert-success";
                    } else {
                        vm.errors = {
                            last_name: response.last_name,
                            first_name: response.first_name
                        };
                        vm.message = "Ошибка : " + response.$status;
                        vm.class = "alert-danger";
                    }
                })
            };

            vm.showProfile = false;
            vm.toggleProfile = function () {
                vm.showProfile = !vm.showProfile;
            };

            vm.acceptInvitation = function (index, accept) {
                var invitation = vm.profile.invitations[index];
                $http.post('api/invitations/', {accept: accept, id: invitation.id})
                    .success(function (response, status, headers, config) {
                        if (accept) {
                            $location.search({eventId: invitation.event.id});
                            vm.toggleProfile();
                            $route.reload();

                        } else {
                            vm.profile.invitations.splice(index, 1);
                        }
                    })
            }

        });
})();
