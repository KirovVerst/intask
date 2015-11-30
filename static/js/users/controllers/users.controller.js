(function () {
	'use strict';

	angular
		.module('application.users.controllers')
		.controller('UsersController', function (Users, $http, $scope, Auth, $window, $routeParams, $uibModal) {

			var vm = this;
			vm.profile = Users.get({id: Auth.getUserId()});

			vm.updateProfile = function () {
				Users.update({id: Auth.getUserId()}, vm.profile);
			}
		});
})();
