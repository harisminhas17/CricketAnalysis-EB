<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;

//Player Auth Routes
Route::post('playerRegister', [AuthController::class, 'playerRegister']);
Route::post('playerLogin', [AuthController::class, 'playerLogin']);
Route::get('getNationalities', [AuthController::class, 'getNationalities']);
Route::get('getPlayerRoles', [AuthController::class, 'getPlayerRoles']);



Route::post('checkCredentials', [AuthController::class, 'checkCredentials']);

Route::middleware('auth:sanctum')->group(function () {

    Route::post('updatePlayerProfile', [AuthController::class, 'updatePlayerProfile']);

});
