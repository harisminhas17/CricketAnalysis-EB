<?php

namespace App\Http\Controllers\Coach;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\Coach;

class CoachController extends Controller
{
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
            'sport_type' => 'required|string|max:100'

        ]);

        try {

            $coachExists = Coach::where('email', $request->email)->exists();

            if ($coachExists) {
                return response()->json([
                    'error'   => true,
                    'message' => 'Email already exists: ' . $request->email
                ], 200);
            }

            $coach = Coach::create([
                'name'       => $request->name,
                'email'      => $request->email,
                'password'   => Hash::make($request->password),
                'phone_number'   => $request->phone,
                'coach_speciality' => $request->speciality,
                'experience_years' => $request->experience,
                'sport_type' => $request->sport_type,
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'error'   => true,
                'message' => 'Error checking email: ' . $e->getMessage()
            ], 200);
        }

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation Error',
                'records' => $validator->errors()
            ], 200);
        }

        return response()->json([
            'error'   => false,
            'message' => 'Coach registered successfully',
            'records' => $coach
        ], 200);
    }

    public function coachLogin(Request $request)
    {
        $request->validate([
            'email'    => 'required|email',
            'password' => 'required|string'
        ]);

        $coach = Coach::where('email', $request->email)->first();

        if (!$coach) {
            return response()->json([
                'error'   => true,
                'message' => 'Coach Email not found',
            ], 200);
        }

        if (!Hash::check($request->password, $coach->password)) {
            return response()->json([
                'error'   => true,
                'message' => 'Password does not match'
            ], 200);
        }

        $token = $coach->createToken('coach-token')->plainTextToken;

        return response()->json([
            'error'   => false,
            'message' => 'Coach Login successful',
            'token'   => $token,
            'records' => $coach
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
        if (Coach::where('email', $request->email)->exists()) {
            return response()->json([
                'error'   => true,
                'message' => 'Coach Email already exists: ' . $request->email
            ], 200);
        }
        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation Error',
                'records' => $validator->errors()
            ], 200);
        }
        $coach = Coach::create([
            'name'       => $request->name,
            'email'      => $request->email,
            'password'   => Hash::make($request->password),
            'phone_number'      => $request->phone,
            'coach_speciality' => $request->speciality,
            'experience_years' => $request->experience,
            'sport_type' => $request->sport_type,
        ]);
        return response()->json([
            'error'   => false,
            'message' => 'Coach added successfully',
            'records' => $coach
        ], 200);
    }
    public function editCoach(Request $request)
    {
        $validated = $request->validate([
            'coach_id'         => 'required',
            'name'       => 'required',
            'email'      => 'sometimes',
            'password'   => 'sometimes',
            'phone_number'      => 'sometimes',
            'coach_speciality' => 'nullable',
            'experience_years' => 'nullable',
            'sport_type' => 'sometimes',

        ]);

        $coach = Coach::where('id', $validated['coach_id'])->first();

        if (!$coach) {
            return response()->json([
                'error'   => true,
                'message' => 'Coach not found with ID: ' . $validated['coach_id']
            ], 200);
        }

        if (isset($validated['password'])) {
            $validated['password'] = Hash::make($validated['password']);
        }

        unset($validated['coach_id']); // Remove coach_id before update

        $coach->update($validated);

        return response()->json([
            'error'   => false,
            'message' => 'Coach updated successfully',
            'records' => $coach
        ], 200);
    }

    public function deleteCoach(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'coach_id' => 'required',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 200);
        }

        $coach = Coach::where('id', $request->coach_id)->first();

        if (!$coach) {
            return response()->json([
                'error'   => true,
                'message' => 'Coach not found with ID: ' . $request->coach_id
            ], 200);
        }

        $coach->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Coach ID: ' . $request->coach_id . ' deleted successfully'
        ], 200);
    }

    public function getAllCoaches(Request $request)
    {
        $coaches = Coach::all();

        if (!$coaches || $coaches->isEmpty()) {
            return response()->json([
                'error'   => true,
                'message' => 'No coaches found'
            ], 200);
        }

        return response()->json([
            'error'   => false,
            'message' => 'All coaches fetched successfully',
            'records' => $coaches
        ], 200);
    }
}
