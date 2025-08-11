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

    // ✅ Admin routes
    Route::get('adminProfile', [SuperAdminController::class, 'adminProfile']);
    Route::post('updateProfile', [SuperAdminController::class, 'updateProfile']);
    Route::post('adminLogout', [SuperAdminController::class, 'adminLogout']); 

    // ✅ Player routes
    Route::post('updatePlayerProfile', [AuthController::class, 'updatePlayerProfile']);
});
