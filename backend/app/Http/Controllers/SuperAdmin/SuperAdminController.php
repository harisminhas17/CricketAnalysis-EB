<?php

namespace App\Http\Controllers\SuperAdmin;

use App\HelperFunctions\HelperFunctions;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\SuperAdmin;
use Illuminate\Support\Facades\Auth;

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
                'message' => 'Admin Email already exists: ' . $request->email
            ], 200);
        }

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation Error',
                'records' => $validator->errors()
            ], 200);
        }

        $admin = SuperAdmin::create([
            'name'         => $request->name,
            'email'        => $request->email,
            'password'     => Hash::make($request->password),
            'phone_number' => $request->phone,
            'address'      => $request->address,
            'nationality'  => $request->nationality,
            'country'     => $request->country,
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
                'message' => 'Admin Email not found',
                'records' => $request->email
            ], 200);
        }

        if (!Hash::check($request->password, $admin->password)) {
            return response()->json([
                'error'   => true,
                'message' => 'Password does not match'
            ], 200);
        }

        $token = $admin->createToken('admin-token')->plainTextToken;

        return response()->json([
            'error'   => false,
            'message' => 'Admin Login successful',
            'token'   => $token,
            'records' => $admin
        ], 200);
    }

    //----------------------Update Admin Profile--------------------------------
    public function updateAdminProfile(Request $request)
    {
        $admin = Auth::user();

        $validator = Validator::make($request->all(), [
            'name'          => 'sometimes|required|string|max:100',
            'phone_number'  => 'nullable|string|max:20',
            'profile_image' => 'nullable',
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
            ], 200);
        }

        if ($request->hasFile('profile_image')) {
            $imagePath = HelperFunctions::uploadImage(
                $request->file('profile_image'),
                'profiles/superadmin'
            );
            $admin->profile_image = $imagePath;
        }

        $updateData = $request->only([
            'name',
            'phone_number',
            'state',
            'city',
            'address',
            'zip_code',
            'country',
            'password'
        ]);

        if ($request->filled('password')) {
            $updateData['password'] = Hash::make($request->password);
        }

        // Add profile_image to updateData if it was processed
        if ($request->hasFile('profile_image')) {
            $updateData['profile_image'] = $admin->profile_image;
        }

        SuperAdmin::where('id', $admin->id)->update($updateData);

        $admin = SuperAdmin::find($admin->id);

        return response()->json([
            'error'   => false,
            'message' => 'Admin Profile updated successfully',
            'records' => $admin
        ]);
    }
}
