<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\SuperAdminController;
use App\Http\Controllers\HawkEye\HawkEyeController;

Route::get('test', [HawkEyeController::class, 'showTestPage']);
Route::post('processTestingClip', [HawkEyeController::class, 'processTestingClip']);
// HawkEye routes moved to api.php
