<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\SuperAdminController;

// Public routes
Route::post('adminRegister', [SuperAdminController::class, 'adminRegister']);
Route::post('adminLogin', [SuperAdminController::class, 'adminLogin']);

// Player Auth Routes
Route::post('playerRegister', [AuthController::class, 'playerRegister']); 
Route::post('playerLogin', [AuthController::class, 'playerLogin']);
Route::get('getNationalities', [AuthController::class, 'getNationalities']);
Route::get('getPlayerRoles', [AuthController::class, 'getPlayerRoles']);
Route::post('checkCredentials', [AuthController::class, 'checkCredentials']);

// Protected routes (Require Sanctum token)
Route::middleware('auth:sanctum')->group(function () {

    //  Admin routes
    Route::get('adminProfile', [SuperAdminController::class, 'adminProfile']);
    Route::post('updateProfile', [SuperAdminController::class, 'updateProfile']);
    Route::post('adminLogout', [SuperAdminController::class, 'adminLogout']);
    //Player routes
    Route::post('addPlayer', [SuperAdminController::class, 'addPlayer']);
    Route::post('editPlayers', [SuperAdminController::class, 'editPlayers']);
    Route::delete('deletePlayer', [AuthController::class, 'deletePlayer']);
    //Teams routes
    Route::post('addTeam', [SuperAdminController::class, 'addTeam']);
    Route::post('editTeam', [SuperAdminController::class, 'editTeam']);
    Route::delete('deleteTeam', [SuperAdminController::class, 'deleteTeam']);
   // Coach Routes
   Route::post('addCoach', [SuperAdminController::class, 'addCoach']);
   Route::post('editCoach', [SuperAdminController::class, 'editCoach']);
   Route::delete('deleteCoach', [SuperAdminController::class, 'deleteCoach']);

  // Club Routes
  Route::post('addClub', [SuperAdminController::class, 'addClub']);
  Route::post('editClub', [SuperAdminController::class, 'editClub']);
  Route::delete('deleteClub', [SuperAdminController::class, 'deleteClub']);

    
    

    // ✅ Player routes
    Route::post('updatePlayerProfile', [AuthController::class, 'updatePlayerProfile']);
});
