angular.module("omxremote", ['ui.bootstrap']);

angular.module('omxremote').controller('ModalInstanceCtrl', function ($scope, $modalInstance) {
    $scope.ok = function () {
        $modalInstance.close();
    };
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

angular.module("omxremote").controller("OmxRemoteCtrl", function ($scope, $modal, $timeout) {

    var playPauseIcon = ["glyphicon-play", "glyphicon-pause"];
    var playPauseText = ["Play", "Pause"];
    var status = 0; // 0=paused, 1=playing

    $scope.playPauseText = playPauseText[status]; 
    $scope.playPauseClass = playPauseIcon[status];

    $scope.filename = "test.avi";
    $scope.position = 0;
    $scope.duration = 0;
    $scope.selectedMovie = 0;

    $scope.movies = [
        {"filename" : "a.avi", "hash" : "asdf1"}, 
        {"filename" : "b.avi", "hash" : "asdf2"}, 
        {"filename" : "c.avi", "hash" : "asdf3"}
    ];

    $scope.togglePlay = function() {
        status = (++status) % 2;
        $scope.playPauseText = playPauseText[status]; 
        $scope.playPauseClass = playPauseIcon[status];
        // pause can be used to toggle play/pause
        $scope.sendCommand('pause');
    }

    $scope.sendCommand = function(cmd) {
        alert(cmd);
    }

    $scope.changeMovie = function() {
        var modalInstance = $modal.open({
          animation: true,
          templateUrl: 'modal.html',
          controller: 'ModalInstanceCtrl',
        });

        modalInstance.result.then(function () {
            alert('ok');
        }, function () {
            alert('cancel');
        });
    }
});


