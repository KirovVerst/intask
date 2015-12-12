/**
 * Created by Kirov on 19/11/15.
 */
(function () {
    'use strict';

    angular.module('application.tasks.controllers')
        .controller('SubtasksController', function (Tasks, Events, Subtasks, $routeParams, $window, Auth, $filter) {

            var orderBy = $filter('orderBy');
            var vm = this;
            vm.currentEvent = Events.get({id: $routeParams.eventId});
            vm.currentTask = Tasks.get({eventId: $routeParams.eventId, taskId: $routeParams.taskId});

            vm.subtasks = Subtasks.query({eventId: $routeParams.eventId});

            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };

            vm.newSubtask = {};

            vm.createSubtask = function () {
                vm.newSubtask.finish_time = dateFormat(new Date(vm.newSubtask.finish_time));
                Tasks.save({eventId: vm.event.id}, vm.newSubtask);
                $window.location = '/events/' + vm.currentEvent.id + '/tasks/' + vm.currentTask.id;
            };

            vm.removeSubtask = function (index) {
                Subtasks.delete({
                    eventId: $routeParams.eventId,
                    taskId: $routeParams.taskId,
                    subtaskId: vm.subtasks[index].id
                });
                vm.subtasks.splice(index, 1);
            };


            vm.orderSubtask = function (predicate) {
                vm.reverse = (vm.predicate === predicate) ? !vm.reverse : false;
                vm.class = vm.reverse ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                vm.predicate = predicate;
                vm.subtasks = orderBy(vm.subtasks, predicate, vm.reverse);
            };

            vm.currentSubtask = false;

            vm.setEditFormSubtask = function (index) {
                vm.currentSubtask = vm.subtasks[index];
            };
            vm.popEditFormSubtask = function () {
                vm.currentSubtask = false;
            };

            vm.updateSubtask = function () {
                vm.currentSubtask = dateFormat(new Date(vm.currentSubtask));
                Subtasks.update({
                    eventId: $routeParams.eventId,
                    taskId: $routeParams.taskId,
                    subtaskId: vm.currentSubtask.id
                }, vm.currentSubtask).$promise.then(function (response) {
                    if (response.$status == 200) {
                        vm.message = "Обновлено";
                        vm.class = "alert-success";
                        vm.errors = null;
                    } else {
                        vm.message = "Ошибка : " + response.$status;
                        vm.class = "alert-danger";
                        vm.errors = null;
                    }
                });
            }


        })
})();
