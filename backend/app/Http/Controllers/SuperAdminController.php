<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\SuperAdmin;
use App\HelperFunctions\HelperFunctions;

class SuperAdminController extends Controller
{
    //----------------------Admin Register----------------
    public function adminRegister(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name'         => 'required|string|max:100',
            'email'        => 'required|string|max:100',
            'password'     => 'required|string|max:100',
            'address'      => 'required|string|max:100',
            'nationality'  => 'required|string|max:100',
            'phone'        => 'required|string|max:100',
        ]);

        if (SuperAdmin::where('email', $request->email)->exists()) {
            return response()->json([
                'error'   => true,
                'message' => 'Email already exists: ' . $request->email
            ], 200);
        }

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation Error',
                'records' => $validator->errors()
            ], 422);
        }

        $admin = SuperAdmin::create([
            'name'         => $request->name,
            'email'        => $request->email,
            'password'     => Hash::make($request->password),
            'phone_number' => $request->phone,
            'address'      => $request->address,
            'nationality'  => $request->nationality,
            'country'     => $request->country ,
            'city'        => $request->city
        ]);

        return response()->json([
            'error'   => false,
            'message' => 'Admin registered successfully!',
            'records' => $admin
        ], 200);
    }

   //----------------------Admin Login----------------
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
                'records' => $request->email
            ], 404);
        }

        if (!Hash::check($request->password, $admin->password)) {
            return response()->json([
                'error'   => true,
                'message' => 'Password does not match'
            ], 401);
        }

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

    //----------------------Admin Profile----------------
    public function adminProfile(Request $request)
    {
        $admin = $request->user();

        return response()->json([
            'error'   => false,
            'message' => 'Admin profile fetched successfully',
            'records' => $admin->only([
                'id', 'name', 'email', 'phone_number', 'profile_image',
                'state', 'city', 'address', 'zip_code', 'country', 'is_active'
            ])
        ], 200);
    }

    //----------------------Update Admin Profile--------------------------------
    public function updateProfile(Request $request)
    {
        $admin = $request->user();

        $validator = Validator::make($request->all(), [
            'name'          => 'sometimes|required|string|max:100',
            'phone_number'  => 'nullable|string|max:20',
            'profile_image' => 'nullable|image|mimes:jpeg,png,jpg,gif|max:2048',
            'state'         => 'nullable|string|max:100',
            'city'          => 'nullable|string|max:100',
            'address'       => 'nullable|string|max:255',
            'zip_code'      => 'nullable|string|max:10',
            'country'       => 'nullable|string|max:100',
            'password'      => 'nullable|string|min:6',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 422);
        }

        if ($request->hasFile('profile_image')) {
            $imagePath = HelperFunctions::uploadImage(
                $request->file('profile_image'),
                'profiles/superadmin'
            );
            $admin->profile_image = $imagePath;
        }

        $admin->fill($request->only([
            'name', 'phone_number', 'state', 'city', 'address', 'zip_code', 'country'
        ]));

        if ($request->filled('password')) {
            $admin->password = Hash::make($request->password);
        }

        $admin->save();

        return response()->json([
            'error'   => false,
            'message' => 'Profile updated successfully',
            'records' => $admin->only([
                'id', 'name', 'email', 'phone_number', 'profile_image',
                'state', 'city', 'address', 'zip_code', 'country', 'is_active'
            ])
        ]);
    }

    //----------------------Logout----------------
    public function adminLogout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Logout successful (current device)'
        ]);
    }
}