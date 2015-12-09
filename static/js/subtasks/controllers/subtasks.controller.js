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

            vm.newTask = {};

            vm.createSubtask = function () {
                vm.newTask.finish_time = dateFormat(new Date(vm.newTask.finish_time));
                Tasks.save({eventId: vm.event.id}, vm.newTask);
                $window.location = '/events/' + vm.event.id;
            };

            vm.removeTask = function (index, tasks) {
                Tasks.delete({eventId: $routeParams.eventId, taskId: tasks[index].id});
                tasks.splice(index, 1);
            };


            vm.orderMyTask = function (predicate) {
                vm.reverseMyTask = (vm.predicateMyTask === predicate) ? !vm.reverseMyTask : false;
                vm.classMyTask = vm.reverseMyTask ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                vm.predicateMyTask = predicate;
                vm.myTasks = orderBy(vm.myTasks, predicate, vm.reverseMyTask);
            };


            vm.orderOtherTask = function (predicate) {
                vm.reverseOtherTask = (vm.predicateOtherTask === predicate) ? !vm.reverseOtherTask : false;
                vm.predicateOtherTask = predicate;
                vm.classOtherTask = vm.reverseOtherTask ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";

                vm.otherTasks = orderBy(vm.otherTasks, predicate, vm.reverseOtherTask);
            };

        })
})();
