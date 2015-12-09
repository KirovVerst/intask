/**
 * Created by Kirov on 19/11/15.
 */
(function () {
    'use strict';

    angular.module('application.tasks.controllers')
        .controller('TasksController', function (Tasks, Events, $routeParams, $window, Auth, $filter) {

            var orderBy = $filter('orderBy');
            var vm = this;
            vm.event = Events.get({id: $routeParams.eventId});

            vm.newTask = {};

            Tasks.query({eventId: $routeParams.eventId}).$promise.then(function (data) {
                var userId = Auth.getUserId();
                vm.myTasks = [];
                vm.otherTasks = [];
                for (var index = 0; index < data.length; ++index) {
                    if (data[index].task_header.id == userId) {
                        vm.myTasks.push(data[index]);
                    }
                    else {
                        vm.otherTasks.push(data[index]);
                    }
                }
            });

            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };

            vm.createTask = function () {
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
