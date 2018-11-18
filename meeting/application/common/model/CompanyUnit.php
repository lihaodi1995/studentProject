<?php
namespace app\common\model;

use think\Model;

class CompanyUnit extends Model {
    protected $pk = 'company_unit_id';

    public function company() {
        return $this->belongsTo('Company');
    }
}
