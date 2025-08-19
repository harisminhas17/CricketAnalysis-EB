<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\SuperAdminController;
use App\Http\Controllers\SuperAdmin\TeamController;
use App\Http\Controllers\SuperAdmin\ClubController;

// General Routes
Route::get('getNationalities', [AuthController::class, 'getNationalities']);
Route::get('getPlayerRoles', [AuthController::class, 'getPlayerRoles']);

// Admin Auth Routes
Route::post('adminRegister', [SuperAdminController::class, 'adminRegister']);
Route::post('adminLogin', [SuperAdminController::class, 'adminLogin']);

// Player Auth Routes
Route::post('playerRegister', [AuthController::class, 'playerRegister']);
Route::post('playerLogin', [AuthController::class, 'playerLogin']);
Route::post('checkCredentials', [AuthController::class, 'checkCredentials']);

// Coach Auth Routes


// Club Auth Routes


// Protected Routes
Route::middleware('auth:sanctum')->group(function () {

    //  Admin routes
    Route::get('adminProfile', [SuperAdminController::class, 'adminProfile']);
    Route::post('updateProfile', [SuperAdminController::class, 'updateProfile']);
    Route::post('adminLogout', [SuperAdminController::class, 'adminLogout']);

    //Player routes
    Route::post('addPlayer', [SuperAdminController::class, 'addPlayer']);
    Route::post('editPlayers', [SuperAdminController::class, 'editPlayers']);
    Route::delete('deletePlayer', [AuthController::class, 'deletePlayer']);
    Route::post('updatePlayerProfile', [AuthController::class, 'updatePlayerProfile']);

    //Teams routes
    Route::post('addTeam', [TeamController::class, 'addTeam']);
    Route::post('editTeam', [TeamController::class, 'editTeam']);
    Route::delete('deleteTeam', [TeamController::class, 'deleteTeam']);

    // Coach Routes
    Route::post('addCoach', [SuperAdminController::class, 'addCoach']);
    Route::post('editCoach', [SuperAdminController::class, 'editCoach']);
    Route::delete('deleteCoach', [SuperAdminController::class, 'deleteCoach']);

    // Club Routes
    Route::post('addClub', [ClubController::class, 'addClub']);
    Route::post('editClub', [ClubController::class, 'editClub']);
    Route::delete('deleteClub', [ClubController::class, 'deleteClub']);
});
