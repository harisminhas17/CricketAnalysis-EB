<?php

namespace App\Http\Controllers\Coach;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\Coach;

class CoachController extends Controller
{
   //----------------------Coach Register----------------
public function coachRegister(Request $request)
{
    $validator = Validator::make($request->all(), [
        'name'         => 'required|string|max:100',
        'email'        => 'required|string|email|max:100',
        'password'     => 'required|string|max:100',
        'phone'        => 'required|string|max:100',
        'speciality'   => 'nullable|string|max:100',
        'experience'   => 'nullable|string|max:100',
        'profile_image' => 'nullable|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
        'sport_type'=>'required|string|max:100'
        
    ]);

    if (\App\Models\Coach::where('email', $request->email)->exists()) {
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

    $coach = \App\Models\Coach::create([
        'name'       => $request->name,
        'email'      => $request->email,
        'password'   => Hash::make($request->password),
        'phone'      => $request->phone,
        'speciality' => $request->speciality,
        'experience' => $request->experience,
        'sport_type' => $request->sport_type,
    ]);

    return response()->json([
        'error'   => false,
        'message' => 'Coach registered successfully!',
        'records' => $coach
    ], 200);
}

//----------------------Coach Login----------------
public function coachLogin(Request $request)
{
    $request->validate([
        'email'    => 'required|email',
        'password' => 'required|string'
    ]);

    $coach = \App\Models\Coach::where('email', $request->email)->first();

    if (!$coach) {
        return response()->json([
            'error'   => true,
            'message' => 'Email not found',
            'records' => $request->email
        ], 404);
    }

    if (!Hash::check($request->password, $coach->password)) {
        return response()->json([
            'error'   => true,
            'message' => 'Password does not match'
        ], 401);
    }

    $token = $coach->createToken('coach-token')->plainTextToken;

    return response()->json([
        'error'   => false,
        'message' => 'Login successful',
        'token'   => $token,
        'records' => $coach->only([
            'id', 'name', 'email', 'phone', 'speciality', 'experience'
        ])
    ], 200);
}
//-------------------Add Coach---------------------
public function addCoach(Request $request)
{
    $validator = Validator::make($request->all(), [
        'name'       => 'required',
        'email'      => 'required',
        'password'   => 'required',
        'phone'      => 'required',
        'speciality' => 'nullable',
        'experience' => 'nullable',
        'sport_type' => 'required',
    ]);
    if (\App\Models\Coach::where('email', $request->email)->exists()) {
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
    $coach = \App\Models\Coach::create([
        'name'       => $request->name,
        'email'      => $request->email,
        'password'   => Hash::make($request->password),
        'phone'      => $request->phone,
        'speciality' => $request->speciality,
        'experience' => $request->experience,
        'sport_type' => $request->sport_type,
    ]);
    return response()->json([
        'error'   => false,
        'message' => 'Coach added successfully!',
        'records' => $coach
    ], 200);
}
//------------------ Edit Coach ---------------------
public function editCoach(Request $request)
{
    $validated = $request->validate([
        'id'         => 'required|integer|exists:coaches,id',
        'name'       => 'required|string|max:100',
        'email'      => 'sometimes|email|unique:coaches,email,' . $request->id,
        'password'   => 'sometimes|string|min:6',
        'phone'      => 'required|string|max:20',
        'speciality' => 'nullable|string|max:100',
        'experience' => 'nullable|string|max:100',
        'address'    => 'required|string|max:255',
        'city'       => 'required|string|max:100',
        'country'    => 'required|string|max:100',
        'dob'        => 'required|date',
        
    ]);

    $coach = \App\Models\Coach::findOrFail($validated['id']);

    if (isset($validated['password'])) {
        $validated['password'] = Hash::make($validated['password']);
    }

    unset($validated['id']); // Remove id before update

    $coach->update($validated);

    return response()->json([
        'error'   => false,
        'message' => 'Coach updated successfully',
        'records' => $coach
    ], 200);
}

//------------------- Delete Coach ---------------------
public function deleteCoach(Request $request)
{
    $validator = Validator::make($request->all(), [
        'id' => 'required|integer|exists:coaches,id',
    ]);

    if ($validator->fails()) {
        return response()->json([
            'error'   => true,
            'message' => 'Validation failed',
            'records' => $validator->errors()
        ], 422);
    }

    $coach = \App\Models\Coach::findOrFail($request->id);
    $coach->delete();

    return response()->json([
        'error'   => false,
        'message' => 'Coach deleted successfully!',
    ], 200);
}
}