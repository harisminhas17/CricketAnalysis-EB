<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\SuperAdminController;

//  Your desired routes:
Route::post('/adminRegister', [SuperAdminController::class, 'adminRegister']);
Route::post('/adminLogin', [SuperAdminController::class, 'adminLogin']);

// Player API routes 
Route::post('/playerRegister', [AuthController::class, 'playerRegister']);
Route::post('/playerLogin', [AuthController::class, 'playerLogin']);