(function () {
    'use strict';


    angular
        .module('application.events.controllers')
        .controller('EventsController', function (Events, $http, $scope, Auth, $window, $routeParams, $filter) {

            var orderBy = $filter('orderBy');

            var vm = this;
            vm.today = new Date();
            vm.isLoggedIn = !!Auth.getToken();
            vm.newEvent = null;

            vm.setNewEvent = function () {
                vm.newEvent = {
                    finish_time: new Date()
                }
            };

            Events.query().$promise.then(function (data) {
                var userId = Auth.getUserId();
                vm.myEvents = [];
                vm.otherEvents = [];
                for (var index = 0; index < data.length; ++index) {
                    if (data[index].event_header.id == userId) {
                        vm.myEvents.push(data[index]);
                    }
                    else {
                        vm.otherEvents.push(data[index]);
                    }
                }
            });
            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };
            vm.createEvent = function () {
                vm.newEvent.event_header = Auth.getUserId();
                vm.newEvent.finish_time = dateFormat(new Date(vm.newEvent.finish_time));
                Events.save(vm.newEvent);
                $window.location = "/";
            };


            vm.deleteEvent = function (index) {
                var event = vm.myEvents[index];
                var f = confirm("Вы действительно хотите удалить событие " + event.title + "?");
                if (f) {
                    var eventId = event.id;
                    vm.myEvents.splice(index, 1);
                    Events.delete({id: eventId});
                }
            };

            vm.redirectToEventPage = function (eventId) {
                $window.location = '/events/' + eventId + '/';
            };

            vm.predicateMyEvent = 'title';
            vm.reverseMyEvent = false;
            vm.orderMyEvent = function (predicate) {
                vm.reverseMyEvent = (vm.predicateMyEvent === predicate) ? !vm.reverseMyEvent : false;
                vm.classMyEvent = vm.reverseMyEvent ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                vm.predicateMyEvent = predicate;
                vm.myEvents = orderBy(vm.myEvents, predicate, vm.reverseMyEvent);
            };

            vm.predicateOtherEvent = 'title';
            vm.reverseOtherEvent = false;
            vm.orderOtherEvent = function (predicate) {
                vm.reverseOtherEvent = (vm.predicateOtherEvent === predicate) ? !vm.reverseOtherEvent : false;
                vm.predicateOtherEvent = predicate;
                vm.otherEvents = orderBy(vm.otherEvents, predicate, vm.reverseOtherEvent);
            };

        });
})();
