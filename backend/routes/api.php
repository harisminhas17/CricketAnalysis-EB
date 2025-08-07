<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\SuperAdminController;

// Public routes
Route::post('/adminRegister', [SuperAdminController::class, 'adminRegister']);
Route::post('/adminLogin', [SuperAdminController::class, 'adminLogin']);

Route::post('/playerRegister', [AuthController::class, 'playerRegister']);
Route::post('/playerLogin', [AuthController::class, 'playerLogin']);

// Protected routes (Require Sanctum token)
Route::middleware('auth:sanctum')->group(function () {
    // ✅ Admin Profile route using controller
    Route::get('/adminProfile', [SuperAdminController::class, 'adminProfile']);
});
