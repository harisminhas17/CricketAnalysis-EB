<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\SuperAdmin;

class SuperAdminController extends Controller
{
    /**
     * ✅ Admin Registration
     */
    public function adminRegister(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name'          => 'required|string|max:100',
            'email'         => 'required|email|unique:super_admin,email',
            'password'      => 'required|string|min:6',
            'phone_number'  => 'nullable|string|max:20',
            'profile_image' => 'nullable|string|max:255',
            'state'         => 'nullable|string|max:100',
            'city'          => 'nullable|string|max:100',
            'address'       => 'nullable|string|max:255',
            'zip_code'      => 'nullable|string|max:10',
            'country'       => 'nullable|string|max:100',
            'is_active'     => 'nullable|boolean'
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

        return response()->json([
            'error'   => false,
            'message' => 'Admin registered successfully!',
            'records' => $admin->only([
                'id', 'name', 'email', 'phone_number', 'profile_image',
                'state', 'city', 'address', 'zip_code', 'country', 'is_active'
            ])
        ], 201);
    }

    /**
     * ✅ Admin Login
     */
    public function adminLogin(Request $request)
    {
        $request->validate([
            'email'    => 'required|email',
            'password' => 'required|string'
        ]);

        $admin = SuperAdmin::where('email', $request->email)->first();

        if (!$admin) {
            return response()->json([
                'error'   => true,
                'message' => 'Email not found',
                'input_email' => $request->email
            ], 404);
        }

        if (!Hash::check($request->password, $admin->password)) {
            return response()->json([
                'error'   => true,
                'message' => 'Password does not match'
            ], 401);
        }

        // ✅ Generate Sanctum token
        $token = $admin->createToken('admin-token')->plainTextToken;

        return response()->json([
            'error'   => false,
            'message' => 'Login successful',
            'token'   => $token,
            'records' => $admin->only([
                'id', 'name', 'email', 'phone_number', 'profile_image',
                'state', 'city', 'address', 'zip_code', 'country', 'is_active'
            ])
        ], 200);
    }

    /**
     * ✅ Admin Profile (Sanctum Protected Route)
     */
    public function adminProfile(Request $request)
    {
        $admin = $request->user(); // Authenticated SuperAdmin via Sanctum

        return response()->json([
            'error'   => false,
            'message' => 'Admin profile fetched successfully',
            'records' => $admin->only([
                'id', 'name', 'email', 'phone_number', 'profile_image',
                'state', 'city', 'address', 'zip_code', 'country', 'is_active'
            ])
        ], 200);
    }
}
