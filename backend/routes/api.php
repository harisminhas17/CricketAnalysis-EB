<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;


Route::post('playerRegister', [AuthController::class, 'playerRegister']);
Route::post('playerLogin', [AuthController::class, 'playerLogin']);

Route::middleware('auth:sanctum')->group(function () {

});
