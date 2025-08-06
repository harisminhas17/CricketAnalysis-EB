<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\SuperAdmin;

class SuperAdminController extends Controller
{
    // ✅ Admin Registration
    public function adminRegister(Request $request)
{
    $validator = Validator::make($request->all(), [
        'name'          => 'required|string|max:100',
        'email'         => 'required|email|unique:super_admins,email',
        'password'      => 'required|string|min:6',
        'phone_number'  => 'nullable|string|max:20',
        'profile_image' => 'nullable|string|max:255',
        'state'         => 'nullable|string|max:100',
        'city'          => 'nullable|string|max:100',
        'address'       => 'nullable|string|max:255',
        'zip_code'      => 'nullable|string|max:10',
        'country'       => 'nullable|string|max:100',
        'is_active'     => 'boolean'
    ]);

    if ($validator->fails()) {
        return response()->json([
            'error'   => true,
            'message' => 'Validation Error',
            'records' => $validator->errors()
        ], 422);
    }

    $admin = SuperAdmin::create([
        'name'          => $request->name,
        'email'         => $request->email,
        'password'      => Hash::make($request->password),
        'phone_number'  => $request->phone_number,
        'profile_image' => $request->profile_image,
        'state'         => $request->state,
        'city'          => $request->city,
        'address'       => $request->address,
        'zip_code'      => $request->zip_code,
        'country'       => $request->country,
        'is_active'     => $request->has('is_active') ? $request->is_active : true,
    ]);

    // Hide password before return
    $admin->makeHidden(['password']);

    return response()->json([
        'error'   => false,
        'message' => 'Admin registered successfully!',
        'records' => $admin
    ], 201);
}
    // ✅ Admin Login
    public function adminLogin(Request $request)
{
    $validator = Validator::make($request->all(), [
        'email'    => 'required|string|email',
        'password' => 'required|string',
    ]);

    if ($validator->fails()) {
        return response()->json([
            'error'   => true,
            'message' => 'Validation Error',
            'records' => $validator->errors()
        ], 422);
    }

    $admin = SuperAdmin::where('email', $request->email)->first();

    if (!$admin || !Hash::check($request->password, $admin->password)) {
        return response()->json([
            'error'   => true,
            'message' => 'Invalid email or password',
            'records' => null
        ], 401);
    }

    $admin->makeHidden(['password']);

    return response()->json([
        'error'   => false,
        'message' => 'Login successful',
        'records' => $admin
    ], 200);
}
}