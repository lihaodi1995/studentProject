<?php
namespace app\common\model;

use think\Model;

class CompanyAddition extends Model {
    protected $pk = 'company_addition_id';

    public function company() {
        return $this->belongsTo('Company');
    }
}
