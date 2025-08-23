<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('players', function (Blueprint $table) {
            $table->id();

            // From controller request
            $table->string('sport_type'); // cricket, football etc.
            $table->string('user_name', 100);
            $table->string('email')->unique();
            $table->string('phone', 20)->nullable()->unique();
            $table->string('password');
            $table->string('login_type'); // google, email, fb, etc.
            $table->enum('gender', ['male', 'female', 'other']);
            $table->date('date_of_birth');
            $table->string('address')->nullable();
            
            // Relations
            $table->unsignedBigInteger('nationality_id')->nullable();
            $table->unsignedBigInteger('player_role_id')->nullable();

            // Profile details
            $table->string('profile_image')->nullable();
            $table->string('batting_style')->nullable();
            $table->string('bowling_style')->nullable();
            $table->string('dominant_hand', 20)->nullable();

            // Extra profile update fields (from updatePlayerProfile)
            $table->string('city', 50)->nullable();
            $table->string('state', 50)->nullable();
            $table->string('zip_code', 10)->nullable();
            $table->string('country', 50)->nullable();

            $table->timestamps();

            
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('players');
    }
};
