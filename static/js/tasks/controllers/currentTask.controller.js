(function () {
    'use strict';

    angular
        .module('application.tasks.controllers')
        .controller('CurrentTaskController', function (Events, Tasks, Subtasks, $http, $scope, Auth, $window, $routeParams, UsersInTask) {
            var vm = this;
            vm.today = new Date();
            vm.isLoggedIn = !!Auth.getToken();
            Tasks.get({eventId: $routeParams.eventId, taskId: $routeParams.taskId}).$promise.then(function (data) {
                vm.currentTask = data;
                vm.currentTask.finish_time = new Date(vm.currentTask.finish_time);
                vm.isTaskHeader = Auth.getUserId() == data.task_header.id;
            });
            Events.get({id: $routeParams.eventId}).$promise.then(function (data) {
                vm.currentEvent = data;
                vm.currentEvent.finish_time = new Date(vm.currentEvent.finish_time);
                vm.isEventHeader = Auth.getUserId() == data.event_header.id;
            });


            vm.users = UsersInTask.query({
                eventId: $routeParams.eventId,
                taskId: $routeParams.taskId
            });

            vm.isThisUser = function (id) {
                return Auth.getUserId() == id;
            };

            vm.newSubtask = false;
            vm.setNewSubtask = function () {
                vm.newSubtask = true;
            };
            vm.popNewSubtask = function () {
                vm.newSubtask = false;
            };


            vm.newUser = null;
            vm.setNewUser = function () {
                vm.newUser = {};
            };
            vm.addUser = function () {

            };

            vm.popNewUser = function () {
                vm.newUser = false;
            };

            vm.editFormTask = false;
            vm.setEditFormTask = function () {
                vm.editFormTask = true;
            };
            vm.popEditFormTask = function () {
                vm.editFormTask = false;
            };
            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };
            vm.updateTask = function () {
                Tasks.update({eventId: vm.currentEvent.id, taskId: vm.currentTask.id}, {
                    title: vm.currentTask.title,
                    description: vm.currentTask.description,
                    finish_time: dateFormat(new Date(vm.currentTask.finish_time)),
                    task_header: parseInt(vm.currentTask.task_header.id),
                    status: vm.currentTask.status,
                    is_public: vm.currentTask.is_public
                }).$promise.then(function (data) {
                    vm.isTaskUpdated = true;
                    vm.result_message = "Изменения сохранены.";
                })
            };

            vm.statuses = ['COMPLETED', 'DELAYED', 'IN_PROGRESS'];

            vm.removeUser = function (index) {
                var user = vm.users[index];
                if (user.id == vm.currentTask.task_header.id) {
                    alert("Нельзя удалить руководителя из задания");
                    return;
                }
                UsersInTask.delete({
                    eventId: $routeParams.eventId,
                    taskId: $routeParams.taskId,
                    userId: user.id
                });
                if (!(vm.isEventHeader || vm.isTaskHeader)) {
                    $window.location = "/";
                }
                vm.users.splice(index, 1);
            };

            vm.subtasks = Subtasks.query({eventId: $routeParams.eventId, taskId: $routeParams.taskId});

            vm.removeSubtask = function (index) {
                var subtask = vm.subtasks[index];
                Subtasks.delete({eventId: $routeParams.eventId, taskId: $routeParams.taskId, subtaskId: subtask.id});
                vm.subtasks.splice(index, 1);
            }

        });
})();
