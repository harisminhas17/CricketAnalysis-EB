<?php

namespace App\Http\Controllers\SuperAdmin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use App\Models\Club;
use Illuminate\Support\Facades\Hash;

class ClubController extends Controller
{
    //------------------ Add Club ---------------------


    public function addClub(Request $request)
{
    try {
        $validated = $request->validate([
            'name'          => 'required|string|max:100',
            'email'         => 'required|email|max:120|unique:clubs,email',
            'password'      => 'required|string|min:6',
            'address'       => 'nullable|string|max:255',
            'phone_number'  => 'nullable|string|max:20',
            'location'      => 'nullable|string|max:255',
            'coach_id'      => 'nullable|exists:coaches,id',
            'profile_image' => 'nullable|image|max:2048',
            'sport_type'    => 'required|in:cricket,football',
            'is_active'     => 'required|boolean',
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
        ], 201);

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
            'club_id'      => 'required|integer|exists:clubs,id',
            'name'         => 'sometimes|string|max:255',
            'email'        => 'sometimes|email|unique:clubs,email,' . $request->club_id,
            'password'     => 'sometimes|string|min:6',
            'address'      => 'required|string',
            'state'        => 'required|string',
            'city'         => 'required|string',
            'zip_code'     => 'required|string',
            'country'      => 'required|string',
            'phone_number' => 'required|string',
            'location'     => 'nullable|string',
            'coach_id'     => 'nullable|integer',
            'profile_image'=> 'nullable|string',
            'sport_type'   => 'required|string',
            'is_active'    => 'required|boolean',
            'instagram_link'=> 'nullable|string',
            'facebook_link'=> 'nullable|string',
            'twitter_link' => 'nullable|string',
            'youtube_link' => 'nullable|string',
        ]);

        $club = Club::findOrFail($validated['club_id']);

        if(isset($validated['password'])) {
            $validated['password'] = Hash::make($validated['password']);
        }

        unset($validated['club_id']);

        $club->update($validated);

        return response()->json([
            'error' => false,
            'message' => 'Club updated successfully',
            'records' => $club
        ]);
    }

    //------------------ Delete Club ---------------------
    public function deleteClub(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'club_id' => 'required|integer|exists:clubs,id',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 422);
        }

        $club = Club::findOrFail($request->club_id);
        $club->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Club deleted successfully',
        ]);
    }
}
