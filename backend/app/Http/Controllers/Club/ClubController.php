<?php

namespace App\Http\Controllers\Club;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\Club;

class ClubController extends Controller
{
    //----------------------Club Register----------------
public function clubRegister(Request $request)
{
    $validator = Validator::make($request->all(), [
        'name'     => 'required|string|max:100',
        'email'    => 'required|string|email|max:100|unique:clubs,email',
        'password' => 'required|string|min:6|max:100',
        'phone'    => 'required|string|max:100',
        'address'  => 'required|string|max:255',
        'city'     => 'required|string|max:100',
        'country'  => 'required|string|max:100',
        'sport_type' => 'required|string|max:100',
    ]);

    if ($validator->fails()) {
        return response()->json([
            'error'   => true,
            'message' => 'Validation Error',
            'records' => $validator->errors()
        ], 422);
    }

    $club = \App\Models\Club::create([
        'name'     => $request->name,
        'email'    => $request->email,
        'password' => Hash::make($request->password),
        'phone'    => $request->phone,
        'address'  => $request->address,
        'city'     => $request->city,
        'country'  => $request->country,
        'sport_type' => $request->sport_type,
    ]);

    return response()->json([
        'error'   => false,
        'message' => 'Club registered successfully!',
        'records' => $club
    ], 200);
}

//----------------------Club Login----------------
public function clubLogin(Request $request)
{
    $request->validate([
        'email'    => 'required|email',
        'password' => 'required|string'
    ]);

    $club = \App\Models\Club::where('email', $request->email)->first();

    if (!$club) {
        return response()->json([
            'error'   => true,
            'message' => 'Email not found',
            'records' => $request->email
        ], 404);
    }

    if (!Hash::check($request->password, $club->password)) {
        return response()->json([
            'error'   => true,
            'message' => 'Password does not match'
        ], 401);
    }

    $token = $club->createToken('club-token')->plainTextToken;

    return response()->json([
        'error'   => false,
        'message' => 'Login successful',
        'token'   => $token,
        'records' => $club->only([
            'id', 'name', 'email', 'phone', 'address', 'city', 'country'
        ])
    ], 200);
}

    //------------------ Add Club ---------------------


    public function addClub(Request $request)
{
    try {
        $validated = $request->validate([
            'name'          => 'required|string|max:100',
            'email'         => 'required|email|max:120|unique:clubs,email',
            'password'      => 'required|string|min:6',
            'address'       => 'required|string|max:255',
            'phone'  => 'required',
            'location'      => 'nullable|string|max:255',
            'coach_id'      => 'nullable|exists:coaches,id',
            'profile_image' => 'nullable|image|max:2048',
            'sport_type'    => 'required|in:cricket,football',
            
        ]);

        // Handle image
        if ($request->hasFile('profile_image')) {
            $validated['profile_image'] = $request->file('profile_image')->store('clubs', 'public');
        }

        // Hash password
        $validated['password'] = Hash::make($validated['password']);

        $club = Club::create($validated);

        return response()->json([
            'error'   => false,
            'message' => 'Club created successfully',
            'records' => $club
        ], 200);

    } catch (\Throwable $e) {
        \Log::error('Add Club Error: '.$e->getMessage(), ['trace' => $e->getTraceAsString()]);
        return response()->json([
            'error'   => true,
            'message' => 'Error creating club: '.$e->getMessage(),
        ], 500);
    }
}


    //------------------ Edit Club ---------------------
    public function editClub(Request $request)
    {
        $validated = $request->validate([
            'id'      => 'required|integer|exists:clubs,id',
            'name'         => 'sometimes|string|max:255',
            'email'        => 'sometimes|email|unique:clubs,email,' . $request->club_id,
            'password'     => 'sometimes|string|min:6',
            'address'      => 'required|string',
            'city'         => 'required|string',
            'country'      => 'required|string',
            'phone' => 'required|string',
            'location'     => 'nullable|string',
            'coach_id'     => 'nullable|integer',
            'sport_type'   => 'required|string',
         
        ]);

        $club = Club::findOrFail($validated['id']);

        if(isset($validated['password'])) {
            $validated['password'] = Hash::make($validated['password']);
        }

        unset($validated['id']);

        $club->update($validated);

        return response()->json([
            'error' => false,
            'message' => 'Club updated successfully',
            'records' => $club
        ] , 200);
    }

    //------------------ Delete Club ---------------------
    public function deleteClub(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'id' => 'required|integer|exists:clubs,id',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 422);
        }

        $club = Club::findOrFail($request->id);
        $club->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Club deleted successfully',
        ],200);
    }
}
