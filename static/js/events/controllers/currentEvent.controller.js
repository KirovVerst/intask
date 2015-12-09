(function () {
    'use strict';

    angular
        .module('application.events.controllers')
        .controller('CurrentEventController', function (Events, $http, $scope, Auth, $window, $routeParams, UsersInEvent) {
            var vm = this;
            vm.today = new Date();
            vm.isLoggedIn = !!Auth.getToken();
            Events.get({id: $routeParams.eventId}).$promise.then(function (data) {
                vm.currentEvent = data;
                vm.currentEvent.finish_time = new Date(vm.currentEvent.finish_time);
                vm.isEventHeader = Auth.getUserId() == data.event_header.id;
            });


            vm.users = UsersInEvent.query({eventId: $routeParams.eventId});

            vm.isThisUser = function (id) {
                return Auth.getUserId() == id;
            };

            vm.newTask = false;
            vm.setNewTask = function () {
                vm.newTask = true;
            };
            vm.popNewTask = function () {
                vm.newTask = null;
            };


            vm.newUser = null;
            vm.setNewUser = function () {
                vm.newUser = {};
            };
            vm.inviteUser = function () {
                UsersInEvent.save({eventId: $routeParams.eventId}, vm.newUser);
                vm.isUserInvited = true;
                $window.location = '/events/' + vm.currentEvent.id + '/';
            };
            vm.popNewUser = function () {
                vm.newUser = null;
            };

            vm.editFormEvent = false;
            vm.setEditFormEvent = function () {
                vm.editFormEvent = true;
            };
            vm.popEditFormEvent = function () {
                vm.editFormEvent = false;
            };
            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };
            vm.updateEvent = function () {
                Events.update({id: vm.currentEvent.id}, {
                    title: vm.currentEvent.title,
                    description: vm.currentEvent.description,
                    finish_time: dateFormat(new Date(vm.currentEvent.finish_time)),
                    event_header: parseInt(vm.currentEvent.event_header.id),
                    status: vm.currentEvent.status
                }).$promise.then(function (data) {
                    vm.isEventUpdated = true;
                    vm.result_message = "Изменения сохранены.";
                })
            };

            vm.statuses = ['COMPLETED', 'DELAYED', 'IN_PROGRESS'];

            vm.removeUser = function (index) {
                var user = vm.users[index];
                if (user.id == vm.currentEvent.event_header.id) {
                    alert("Нельзя удалить руководителя из события");
                    return;
                }
                UsersInEvent.delete({eventId: $routeParams.eventId, userId: user.id});
                if (!vm.isEventHeader) {
                    $window.location = "/";
                }
                vm.users.splice(index, 1);
            };

            vm.removeInvitedUser = function (index) {
                var email = vm.currentEvent.invited_users[index];
                $http.post('api/events/' + vm.currentEvent.id + '/invited_users/', {email: email}).success(function (data) {
                    vm.currentEvent.invited_users.splice(index, 1);
                })
            }


        });
})();
